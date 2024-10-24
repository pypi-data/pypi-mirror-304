# Copyright 2023 The EASYDEL Author @erfanzar (Erfan Zare Chavoshi).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# impl from attn 2 paper by @erfanzar, (inspired by org impl by @Dao-AILab)

import functools
import math
import os

os.environ["XLA_PYTHON_CLIENT_PREALLOCATE"] = "false"
os.environ["XLA_PYTHON_CLIENT_MEM_FRACTION"] = "1.0"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["JAX_TRACEBACK_FILTERING"] = "off"

from typing import Optional

import chex
import jax
import numpy as np
import triton
from jax import custom_vjp, random as jrnd
from jax import numpy as jnp
from triton import language as tl

from jax_flash_attn2._custom_call_lib import triton_call

FLASH_ATTN_BWD_ = True
FLASH_ATTN_WRAPS = int(os.environ.get("FLASH_ATTN_WRAPS", "0"))


def calculate_num_warps(
	head_dim: int, q_block_size: int = 0, k_block_size: int = 0
) -> int:
	"""
	Calculate the number of warps based on head dimension and block sizes.

	Args:
	head_dim (int): The dimension of the attention head.
	q_block_size (int): The size of the query block. Default is 0.
	k_block_size (int): The size of the key block. Default is 0.

	Returns:
	int: The number of warps.
	"""
	if 16 < head_dim < 64:
		return 8
	elif 64 < head_dim < 128:
		return 4
	else:
		if q_block_size > 32 and k_block_size > 64:
			return 1
		elif q_block_size > 64 and k_block_size > 32:
			return 1
		else:
			return 4


def _simp_attn(
	query: chex.Array,
	key: chex.Array,
	value: chex.Array,
	bias: Optional[chex.Array],
	softmax_scale: float,
) -> chex.Array:
	"""Simplified attention function for testing and comparison.

	Args:
		query: Query array of shape (..., num_heads, seq_len_q, head_dim).
		key: Key array of shape (..., num_heads, seq_len_k, head_dim).
		value: Value array of shape (..., num_heads, seq_len_k, head_dim).
		bias: Optional bias array of shape (..., num_heads, seq_len_q, seq_len_k).
		softmax_scale: Scaling factor for the softmax function.

	Returns:
		Output array of shape (..., num_heads, seq_len_q, head_dim).
	"""
	dtype = query.dtype
	assert query.ndim == key.ndim, "q, k must have same rank."
	assert query.shape[:-3] == key.shape[:-3], "q, k batch dims must match."
	assert query.shape[-2] == key.shape[-2], "q, k num_heads must match."
	assert query.shape[-1] == key.shape[-1], "q, k depths must match."
	query = query * softmax_scale
	attn_weights = jnp.einsum("...qhd,...khd->...hqk", query, key)
	if bias is not None:
		attn_weights = attn_weights + bias
	attn_weights = jax.nn.softmax(attn_weights).astype(dtype)
	return jnp.einsum("...hqk,...khd->...qhd", attn_weights, value)


def get_strides(shape: tuple[int, ...]) -> tuple[int, ...]:
	"""Calculates strides for a given shape.

	Args:
		shape: Shape of the array.

	Returns:
		Tuple of strides.
	"""
	size = np.prod(shape)
	strides = []
	for s in shape:
		size = int(size // s)
		strides.append(size)
	return tuple(strides)


def get_sharding(arr: chex.Array):
	"""Gets the sharding of an array.

	Args:
		arr: Array to get sharding from.

	Returns:
		Sharding of the array.
	"""
	return getattr(arr, "sharding", None)


def check_shapes_and_dtypes(
	query: chex.Array,
	key: chex.Array,
	value: chex.Array,
	batch: int,
	seqlen_k: int,
	nheads: int,
	headdim: int,
	blocksize_k: int,
	blocksize_q: int,
):
	"""Checks the shapes and dtypes of the input arrays.

	Args:
		query: Query array.
		key: Key array.
		value: Value array.
		batch: Batch size.
		seqlen_k: Sequence length of the key.
		nheads: Number of heads.
		headdim: Head dimension.
		blocksize_k: Block size for the key.
		blocksize_q: Block size for the query.

	Raises:
		AssertionError: If the shapes or dtypes are not valid.
	"""
	chex.assert_shape(
		key,
		(batch, seqlen_k, nheads, headdim),
		custom_message="Shape mismatch for key.",
	)
	chex.assert_shape(
		value,
		(batch, seqlen_k, nheads, headdim),
		custom_message="Shape mismatch for value.",
	)
	chex.assert_equal(
		query.dtype, key.dtype, custom_message="Dtype mismatch between query and key."
	)
	chex.assert_equal(
		key.dtype, value.dtype, custom_message="Dtype mismatch between key and value."
	)
	if query.dtype not in [jnp.float16]:
		raise AssertionError("Only fp16 is supported.") from None
	chex.assert_is_divisible(
		blocksize_k, 16, custom_message="blocksize_k should be divisible by 16."
	)
	chex.assert_is_divisible(
		blocksize_q, 16, custom_message="blocksize_q should be divisible by 16."
	)
	if headdim > 256:
		raise AssertionError("Unsupported headdim value.")


@triton.heuristics(
	{
		"EVEN_N": lambda args: args["seqlen_k"] % args["BLOCK_N"] == 0,
	}
)
@triton.jit
def _fwd_attn_kernel_block_ptr(
	Q,
	K,
	V,
	B,
	softmax_scale: tl.constexpr,
	stride_qb,
	stride_qh,
	stride_qm,
	stride_kb,
	stride_kh,
	stride_kn,
	stride_vb,
	stride_vh,
	stride_vn,
	stride_bb,
	stride_bh,
	stride_bm,
	stride_bn,
	stride_ob,
	stride_oh,
	stride_om,
	stride_lb,
	stride_lh,
	headdim: tl.constexpr,
	nheads: tl.constexpr,
	seqlen_q,
	seqlen_k,
	O,
	L,
	HAVE_BIAS: tl.constexpr,
	BIAS_SINGLE_HEAD: tl.constexpr,
	BLOCK_HEADDIM: tl.constexpr,
	EVEN_N: tl.constexpr,
	BLOCK_M: tl.constexpr,
	BLOCK_N: tl.constexpr,
):
	start_m, off_bh = (
		tl.program_id(0),
		tl.program_id(1),
	)
	off_h = off_bh % nheads
	off_b = off_bh // nheads
	if not EVEN_N:
		offs_n = tl.arange(0, BLOCK_N)

	Q_Block_ptr = tl.make_block_ptr(
		base=Q + (off_b * stride_qb + off_h * stride_qh),
		shape=(seqlen_q, headdim),
		block_shape=(BLOCK_M, BLOCK_HEADDIM),
		strides=(stride_qm, 1),
		offsets=(start_m * BLOCK_M, 0),
		order=(0, 1),
	)
	O_Block_ptr = tl.make_block_ptr(
		base=O + (off_b * stride_ob + off_h * stride_oh),
		shape=(seqlen_q, headdim),
		block_shape=(BLOCK_M, BLOCK_HEADDIM),
		strides=(stride_om, 1),
		offsets=(start_m * BLOCK_M, 0),
		order=(0, 1),
	)
	L_Block_ptr = tl.make_block_ptr(
		base=L + (off_b * stride_lb + off_h * stride_lh),
		shape=(seqlen_q,),
		strides=(1,),
		offsets=(start_m * BLOCK_M,),
		block_shape=(BLOCK_M,),
		order=(0,),
	)
	kv_stride = off_b * stride_kb + off_h * stride_kh
	K_Block_ptr = tl.make_block_ptr(
		base=K + kv_stride,
		shape=(headdim, seqlen_k),
		block_shape=(BLOCK_HEADDIM, BLOCK_N),
		strides=(1, stride_kn),
		offsets=(0, 0),
		order=(1, 0),
	)
	V_Block_ptr = tl.make_block_ptr(
		base=V + kv_stride,
		shape=(seqlen_k, headdim),
		block_shape=(BLOCK_N, BLOCK_HEADDIM),
		strides=(stride_vn, 1),
		offsets=(0, 0),
		order=(0, 1),
	)
	q = tl.load(Q_Block_ptr, boundary_check=(0, 1))
	softmax_scale = softmax_scale.to(tl.float32)
	if HAVE_BIAS:
		bias_h_pos: tl.constexpr = 0 if BIAS_SINGLE_HEAD else off_h
		B_Block_ptr = tl.make_block_ptr(
			base=B + (off_b * stride_bb + bias_h_pos * stride_bh),
			shape=(seqlen_q, seqlen_k),
			block_shape=(BLOCK_M, BLOCK_N),
			strides=(stride_bm, stride_bn),
			offsets=(start_m * BLOCK_M, 0),
			order=(0, 1),
		)
	lse_i = tl.zeros([BLOCK_M], dtype=tl.float32) - float("inf")
	max_i = tl.zeros([BLOCK_M], dtype=tl.float32) - float("inf")
	acc_o = tl.zeros([BLOCK_M, BLOCK_HEADDIM], dtype=tl.float32)
	for j in range(0, seqlen_k, BLOCK_N):
		j = tl.multiple_of(j, BLOCK_N)
		k = tl.load(K_Block_ptr, boundary_check=(0, 1))
		qk = tl.zeros([BLOCK_M, BLOCK_N], dtype=tl.float32)
		qk += tl.dot(q, k) * softmax_scale
		if not EVEN_N:
			qk += tl.where((j + offs_n)[None, :] < seqlen_k, 0, float("-inf")).to(tl.float32)
		if HAVE_BIAS:
			b = tl.load(B_Block_ptr, boundary_check=(0, 1)).to(tl.float32)
			B_Block_ptr = tl.advance(B_Block_ptr, (0, BLOCK_N))
			qk = qk + b
			max_ij = tl.maximum(tl.max(qk, 1), lse_i)
			p = tl.exp(qk - max_ij[:, None])
		else:
			max_ij = tl.maximum(tl.max(qk, 1), lse_i)
			p = tl.exp(qk - max_ij[:, None])
		l_ij = tl.sum(p, 1)
		acc_o_scale = tl.exp(max_i - max_ij)
		acc_o = acc_o * acc_o_scale[:, None]
		v = tl.load(V_Block_ptr, boundary_check=(0, 1))
		acc_o += tl.dot(p.to(v.dtype), v)
		max_i = max_ij
		lse_i = max_ij + tl.log(tl.exp(lse_i - max_ij) + l_ij)
		K_Block_ptr = tl.advance(K_Block_ptr, (0, BLOCK_N))
		V_Block_ptr = tl.advance(V_Block_ptr, (BLOCK_N, 0))

	o_scale = tl.exp(max_i - lse_i)
	acc_o = acc_o * o_scale[:, None]
	tl.store(L_Block_ptr, lse_i, boundary_check=(0,))
	tl.store(O_Block_ptr, acc_o.to(q.dtype), boundary_check=(0, 1))


@triton.heuristics(
	{
		"EVEN_N": lambda args: args["seqlen_k"] % args["BLOCK_N"] == 0,
	}
)
@triton.jit
def _fwd_attn_kernel_ptr_block(
	Q,
	K,
	V,
	B,
	softmax_scale: tl.constexpr,
	stride_qb,
	stride_qh,
	stride_qm,
	stride_kb,
	stride_kh,
	stride_kn,
	stride_vb,
	stride_vh,
	stride_vn,
	stride_bb,
	stride_bh,
	stride_bm,
	stride_bn,
	stride_ob,
	stride_oh,
	stride_om,
	stride_lb,
	stride_lh,
	headdim: tl.constexpr,
	nheads: tl.constexpr,
	seqlen_q,
	seqlen_k,
	O,
	L,
	HAVE_BIAS: tl.constexpr,
	BIAS_SINGLE_HEAD: tl.constexpr,
	BLOCK_HEADDIM: tl.constexpr,
	EVEN_N: tl.constexpr,
	BLOCK_M: tl.constexpr,
	BLOCK_N: tl.constexpr,
):
	start_m, off_bh = (
		tl.program_id(0),
		tl.program_id(1),
	)
	off_h = off_bh % nheads
	off_b = off_bh // nheads
	offs_m = start_m * BLOCK_M + tl.arange(0, BLOCK_M)
	offs_n = tl.arange(0, BLOCK_N)
	offs_d = tl.arange(0, BLOCK_HEADDIM)

	q_ptrs = (
		Q
		+ (off_b * stride_qb + off_h * stride_qh)
		+ (offs_m[:, None] * stride_qm + offs_d[None, :])
	)
	o_ptrs = (
		O
		+ (off_b * stride_ob + off_h * stride_oh)
		+ (offs_m[:, None] * stride_om + offs_d[None, :])
	)
	l_ptrs = L + (off_b * stride_lb + off_h * stride_lh + offs_m)
	k_ptrs = (
		K
		+ (off_b * stride_kb + off_h * stride_kh)
		+ (offs_n[:, None] * stride_kn + offs_d[None, :])
	)
	v_ptrs = (
		V
		+ (off_b * stride_vb + off_h * stride_vh)
		+ (offs_n[:, None] * stride_vn + offs_d[None, :])
	)
	q = tl.load(
		q_ptrs,
		mask=(offs_m[:, None] < seqlen_q) & (offs_d[None, :] < headdim),
		other=0.0,
	)
	softmax_scale = softmax_scale.to(tl.float32)
	if HAVE_BIAS:
		bias_h_pos: tl.constexpr = 0 if BIAS_SINGLE_HEAD else off_h
		b_ptrs = (
			B
			+ (off_b * stride_bb + bias_h_pos * stride_bh)
			+ (offs_m[:, None] * stride_bm + offs_n[None, :] * stride_bn)
		)
	lse_i = tl.zeros([BLOCK_M], dtype=tl.float32) - float("inf")
	max_i = tl.zeros([BLOCK_M], dtype=tl.float32) - float("inf")
	acc_o = tl.zeros([BLOCK_M, BLOCK_HEADDIM], dtype=tl.float32)
	for j in range(0, seqlen_k, BLOCK_N):
		j = tl.multiple_of(j, BLOCK_N)
		current_k = offs_n + j
		k = tl.load(
			k_ptrs + j * stride_kn,
			mask=(current_k[:, None] < seqlen_k) & (offs_d[None, :] < headdim),
			other=0.0,
		)
		qk = tl.zeros([BLOCK_M, BLOCK_N], dtype=tl.float32)
		qk += tl.dot(q, k.T) * softmax_scale
		if not EVEN_N:
			qk += tl.where((j + offs_n)[None, :] < seqlen_k, 0, float("-inf")).to(tl.float32)
		if HAVE_BIAS:
			b = tl.load(
				b_ptrs + j,
				mask=(offs_m[:, None] < seqlen_q) & (current_k[None, :] < seqlen_k),
				other=0.0,
			).to(tl.float32)
			qk = qk + b
			max_ij = tl.maximum(tl.max(qk, 1), lse_i)
			p = tl.exp(qk - max_ij[:, None])
		else:
			max_ij = tl.maximum(tl.max(qk, 1), lse_i)
			p = tl.exp(qk - max_ij[:, None])
		l_ij = tl.sum(p, 1)
		acc_o_scale = tl.exp(max_i - max_ij)
		acc_o = acc_o * acc_o_scale[:, None]
		v = tl.load(
			v_ptrs + j * stride_vn,
			mask=(current_k[:, None] < seqlen_k) & (offs_d[None, :] < headdim),
			other=0.0,
		)
		acc_o += tl.dot(p.to(v.dtype), v)
		max_i = max_ij
		lse_i = max_ij + tl.log(tl.exp(lse_i - max_ij) + l_ij)

	o_scale = tl.exp(max_i - lse_i)
	acc_o = acc_o * o_scale[:, None]
	tl.store(l_ptrs, lse_i, mask=offs_m < seqlen_q)
	tl.store(
		o_ptrs,
		acc_o.to(q.dtype),
		mask=(offs_m[:, None] < seqlen_q) & (offs_d[None, :] < headdim),
	)


def _fwd_attn_kernel_call(
	query: Optional[chex.Array],
	key: Optional[chex.Array],
	value: Optional[chex.Array],
	bias: Optional[chex.Array] = None,
	softmax_scale: Optional[float] = None,
	blocksize_q: int = 128,
	blocksize_k: int = 128,
):
	"""Calls the Triton kernel for the forward pass of the attention mechanism.

	Args:
		query: Query array.
		key: Key array.
		value: Value array.
		bias: Bias array.
		softmax_scale: Scaling factor for the softmax function.
		blocksize_q: Block size for the query sequence dimension.
		blocksize_k: Block size for the key sequence dimension.

	Returns:
		Tuple of the output array and the log-sum-exp array.
	"""
	kernel = (
		_fwd_attn_kernel_block_ptr
		if os.environ.get("FLASH_ATTN_BLOCK_PTR", "0") == "1"
		else _fwd_attn_kernel_ptr_block
	)
	batch, seqlen_q, nheads, headdim = query.shape
	_, seqlen_k, _, _ = key.shape
	check_shapes_and_dtypes(
		query=query,
		key=key,
		value=value,
		batch=batch,
		seqlen_k=seqlen_k,
		nheads=nheads,
		headdim=headdim,
		blocksize_k=blocksize_k,
		blocksize_q=blocksize_q,
	)
	softmax_scale = softmax_scale or 1.0 / math.sqrt(headdim)
	HAVE_BIAS = True if bias is not None else False
	BIAS_SINGLE_HEAD = True if bias is None else (True if bias.shape[1] == 1 else False)
	BLOCK_HEADDIM = max(triton.next_power_of_2(headdim), 16)
	stride_bb, stride_bh, stride_bm, stride_bn = (
		get_strides(bias.shape) if HAVE_BIAS else (0, 0, 0, 0)
	)
	stride_lb, stride_lh, stride_lm = get_strides((batch, nheads, seqlen_q))
	metaparams = dict(
		HAVE_BIAS=HAVE_BIAS,
		BIAS_SINGLE_HEAD=BIAS_SINGLE_HEAD,
		BLOCK_HEADDIM=BLOCK_HEADDIM,
		BLOCK_M=blocksize_q,
		BLOCK_N=blocksize_k,
	)

	stride_qb, stride_qm, stride_qh, stride_qd = get_strides(query.shape)
	stride_kb, stride_kn, stride_kh, stride_kd = get_strides(key.shape)
	stride_vb, stride_vn, stride_vh, stride_vd = get_strides(value.shape)
	num_warps = calculate_num_warps(headdim, blocksize_q, blocksize_k)
	return triton_call(
		query,
		key,
		value,
		bias if bias is not None else jnp.zeros((1,), jnp.float16),
		softmax_scale,
		stride_qb,
		stride_qh,
		stride_qm,
		stride_kb,
		stride_kh,
		stride_kn,
		stride_vb,
		stride_vh,
		stride_vn,
		stride_bb,
		stride_bh,
		stride_bm,
		stride_bn,
		stride_qb,
		stride_qh,
		stride_qm,
		stride_lb,
		stride_lh,
		headdim,
		nheads,
		seqlen_q,
		seqlen_k,
		kernel=kernel,
		out_shape=[
			jax.ShapeDtypeStruct(query.shape, query.dtype, sharding=get_sharding(query)),
			jax.ShapeDtypeStruct((batch, nheads, seqlen_q), jnp.float32),
		],
		grid=lambda META: (triton.cdiv(seqlen_q, META["BLOCK_M"]), batch * nheads, 1),
		name="triton::ops::_fwd_attn_kernel",
		num_stages=1,
		num_warps=num_warps,
		**metaparams,
	)


@triton.jit
def _bwd_do_attn_kernel(
	O,
	Do,
	De,
	stride_ob: int,
	stride_om: int,
	stride_oh: int,
	stride_dob: int,
	stride_dom: int,
	stride_doh: int,
	stride_deb: int,
	stride_deh: int,
	nheads: int,
	headdim: int,
	seqlen_q: int,
	BLOCK_M: tl.constexpr,
	BLOCK_HEADDIM: tl.constexpr,
):
	"""Triton kernel for the backward pass of the attention mechanism with respect to the output gradient.

	Args:
		O: Output array.
		Do: Output gradient array.
		De: Delta array.
		stride_ob: Stride for the output batch dimension.
		stride_om: Stride for the output sequence dimension.
		stride_oh: Stride for the output head dimension.
		stride_dob: Stride for the output gradient batch dimension.
		stride_dom: Stride for the output gradient sequence dimension.
		stride_doh: Stride for the output gradient head dimension.
		stride_deb: Stride for the delta batch dimension.
		stride_deh: Stride for the delta head dimension.
		nheads: Number of heads.
		headdim: Head dimension.
		seqlen_q: Sequence length of the query.
		BLOCK_M: Block size for the query sequence dimension.
		BLOCK_HEADDIM: Block size for the head dimension.
	"""
	off_q = tl.program_id(0)
	off_bh = tl.program_id(1)
	off_b = off_bh // nheads
	off_h = off_bh % nheads
	offs_m = off_q * BLOCK_M + tl.arange(0, BLOCK_M)
	offs_d = tl.arange(0, BLOCK_HEADDIM)
	o_ptrs = (
		O
		+ off_b * stride_ob
		+ off_h * stride_oh
		+ offs_m[:, None] * stride_om
		+ offs_d[None, :]
	)
	do_ptrs = (
		Do
		+ off_b * stride_dob
		+ off_h * stride_doh
		+ offs_m[:, None] * stride_dom
		+ offs_d[None, :]
	)
	o = tl.load(
		o_ptrs,
		mask=(offs_m[:, None] < seqlen_q) & (offs_d[None, :] < headdim),
		other=0.0,
	).to(tl.float32)
	do = tl.load(
		do_ptrs,
		mask=(offs_m[:, None] < seqlen_q) & (offs_d[None, :] < headdim),
		other=0.0,
	).to(tl.float32)
	delta = tl.sum(o * do, axis=1)
	tl.store(
		De + (off_b * stride_deb + off_h * stride_deh + offs_m),
		delta,
		mask=offs_m < seqlen_q,
	)


@triton.heuristics(
	{
		"EVEN_M": lambda args: args["seqlen_q"] % args["BLOCK_M"] == 0,
		"EVEN_N": lambda args: args["seqlen_k"] % args["BLOCK_N"] == 0,
		"EVEN_HEADDIM": lambda args: args["headdim"] == args["BLOCK_HEADDIM"],
	}
)
@triton.jit
def _bwd_attn_kernel(
	Q,
	K,
	V,
	B,
	Do,
	L,
	D,
	softmax_scale: float,
	stride_qb: int,
	stride_qm: int,
	stride_qh: int,
	stride_kb: int,
	stride_kn: int,
	stride_kh: int,
	stride_vb: int,
	stride_vn: int,
	stride_vh: int,
	stride_bb: int,
	stride_bh: int,
	stride_bm: int,
	stride_dob: int,
	stride_dom: int,
	stride_doh: int,
	stride_dqb: int,
	stride_dqm: int,
	stride_dqh: int,
	stride_dkb: int,
	stride_dkn: int,
	stride_dkh: int,
	stride_dvb: int,
	stride_dvn: int,
	stride_dvh: int,
	stride_lb: int,
	stride_lh: int,
	seqlen_q: int,
	seqlen_k: int,
	headdim: int,
	nheads: int,
	Dq: chex.Array,
	Dk: chex.Array,
	Dv: chex.Array,
	HAVE_BIAS: tl.constexpr,
	BIAS_SINGLE_HEAD: tl.constexpr,
	BLOCK_HEADDIM: tl.constexpr,
	EVEN_M: tl.constexpr,
	EVEN_N: tl.constexpr,
	EVEN_HEADDIM: tl.constexpr,
	BLOCK_M: tl.constexpr,
	BLOCK_N: tl.constexpr,
):
	start_n, off_bh = (
		tl.program_id(0),
		tl.program_id(2),
	)
	softmax_scale = softmax_scale.to(tl.float32)
	off_h = off_bh % nheads
	off_b = off_bh // nheads
	offs_qm = tl.arange(0, BLOCK_M)
	offs_n = start_n * BLOCK_N + tl.arange(0, BLOCK_N)
	offs_m = tl.arange(0, BLOCK_M)
	offs_d = tl.arange(0, BLOCK_HEADDIM)
	l_ptrs = L + (off_b * stride_lb + off_h * stride_lh + offs_qm)
	d_ptrs = D + (off_b * stride_lb + off_h * stride_lh + offs_qm)
	q_ptrs = (
		Q
		+ (off_b * stride_qb + off_h * stride_qh)
		+ (offs_qm[:, None] * stride_qm + offs_d[None, :])
	)
	k_ptrs = (
		K
		+ (off_b * stride_kb + off_h * stride_kh)
		+ (offs_n[:, None] * stride_kn + offs_d[None, :])
	)
	v_ptrs = (
		V
		+ (off_b * stride_vb + off_h * stride_vh)
		+ (offs_n[:, None] * stride_vn + offs_d[None, :])
	)
	do_ptrs = (
		Do
		+ (off_b * stride_dob + off_h * stride_doh)
		+ (offs_qm[:, None] * stride_dom + offs_d[None, :])
	)
	dq_ptrs = (
		Dq
		+ (off_b * stride_dqb + off_h * stride_dqh)
		+ (offs_qm[:, None] * stride_dqm + offs_d[None, :])
	)
	if HAVE_BIAS:
		bias_h_pos: tl.constexpr = 0 if BIAS_SINGLE_HEAD else off_h
		b_ptrs = (
			B
			+ (off_b * stride_bb + bias_h_pos * stride_bh)
			+ (offs_qm[:, None] * stride_bm + offs_n[None, :])
		)
	dv = tl.zeros([BLOCK_N, BLOCK_HEADDIM], dtype=tl.float32)
	dk = tl.zeros([BLOCK_N, BLOCK_HEADDIM], dtype=tl.float32)
	k = tl.load(
		k_ptrs,
		mask=(offs_n[:, None] < seqlen_k) & (offs_d[None, :] < headdim),
		other=0.0,
	)
	v = tl.load(
		v_ptrs,
		mask=(offs_n[:, None] < seqlen_k) & (offs_d[None, :] < headdim),
		other=0.0,
	)

	num_block_m = tl.cdiv(seqlen_q, BLOCK_M)
	for start_m in range(0, num_block_m * BLOCK_M, BLOCK_M):
		start_m = tl.multiple_of(start_m, BLOCK_M)
		offs_m_curr = start_m + offs_m
		q = tl.load(
			q_ptrs,
			mask=(offs_m_curr[:, None] < seqlen_q) & (offs_d[None, :] < headdim),
			other=0.0,
		)
		qk = tl.dot(q, k.T) * softmax_scale
		if not EVEN_N:
			qk = tl.where(offs_n[None, :] < seqlen_k, qk, float("-inf"))

		if HAVE_BIAS:
			bias = tl.load(
				b_ptrs,
				mask=(offs_m_curr[:, None] < seqlen_q) & (offs_n[None, :] < seqlen_k),
				other=0.0,
			).to(tl.float32)
			qk = qk + bias
		lse_i = tl.load(l_ptrs + start_m, mask=offs_m_curr < seqlen_q, other=0.0)

		p = tl.exp(qk - lse_i[:, None])
		do = tl.load(
			do_ptrs,
			mask=(offs_m_curr[:, None] < seqlen_q) & (offs_d[None, :] < headdim),
			other=0.0,
		)
		dv += tl.dot(p.to(do.dtype).T, do)
		dp = tl.dot(do, v.T)

		Di = tl.load(d_ptrs + start_m, mask=offs_m_curr < seqlen_q, other=0.0)
		ds = (p * (dp - Di[:, None]) * softmax_scale).to(q.dtype)
		dk += tl.dot(ds.T, q)

		dq = tl.dot(ds, k)
		tl.atomic_add(
			dq_ptrs,
			dq,
			mask=(offs_m_curr[:, None] < seqlen_q) & (offs_d[None, :] < headdim),
		)
		# ADVANCE TO NEXT POINT
		dq_ptrs += BLOCK_M * stride_dqm
		q_ptrs += BLOCK_M * stride_qm
		do_ptrs += BLOCK_M * stride_dom
		if HAVE_BIAS:
			b_ptrs += BLOCK_M * stride_bm
	dv_ptrs = (
		Dv
		+ (off_b * stride_dvb + off_h * stride_dvh)
		+ (offs_n[:, None] * stride_dvn + offs_d[None, :])
	)
	dk_ptrs = (
		Dk
		+ (off_b * stride_dkb + off_h * stride_dkh)
		+ (offs_n[:, None] * stride_dkn + offs_d[None, :])
	)

	tl.store(dv_ptrs, dv, mask=(offs_n[:, None] < seqlen_k) & (offs_d[None, :] < headdim))
	tl.store(dk_ptrs, dk, mask=(offs_n[:, None] < seqlen_k) & (offs_d[None, :] < headdim))


def _bwd_attn_kernel_call(
	softmax_scale: float,
	blocksize_q: int,
	blocksize_k: int,
	residual,
	Do: chex.Array,
):
	"""Calls the Triton kernel for the backward pass of the attention mechanism.

	Args:
		softmax_scale: Scaling factor for the softmax function.
		blocksize_q: Block size for the query sequence dimension.
		blocksize_k: Block size for the key sequence dimension.
		residual: Residual from the forward pass.
		Do: Output gradient array.

	Returns:
		Tuple of the gradients of the query, key, value, and bias arrays.
	"""
	(o, l, query, key, value, bias) = residual
	batch, seqlen_q, nheads, headdim = query.shape
	_, seqlen_k, _, _ = key.shape
	assert key.shape == (
		batch,
		seqlen_k,
		nheads,
		headdim,
	), "shape missmatch between key, value."
	assert value.shape == (
		batch,
		seqlen_k,
		nheads,
		headdim,
	), "shape missmatch between key, value."
	softmax_scale = softmax_scale or 1.0 / math.sqrt(headdim)
	if FLASH_ATTN_BWD_:
		assert headdim <= 256, "given headdim is not supported."
		assert query.dtype == key.dtype == value.dtype, "tensors must have the same dtype."
		assert query.dtype in [jnp.float16], "only support fp16."
		HAVE_BIAS = True if bias is not None else False
		BIAS_SINGLE_HEAD = True if bias is None else (True if bias.shape[1] == 1 else False)
		BLOCK_HEADDIM = max(triton.next_power_of_2(headdim), 16)
		bwd_kernel_out_shapes = [
			jax.ShapeDtypeStruct(
				shape=query.shape,
				dtype=query.dtype,
				sharding=get_sharding(query),
			),
			jax.ShapeDtypeStruct(
				shape=key.shape,
				dtype=key.dtype,
				sharding=get_sharding(key),
			),
			jax.ShapeDtypeStruct(
				shape=value.shape,
				dtype=value.dtype,
				sharding=get_sharding(value),
			),
		]

		delta = jnp.empty_like(l)
		stride_bb, stride_bh, stride_bm = (
			get_strides(bias.shape)[:-1] if HAVE_BIAS else (0, 0, 0)
		)

		# BATCH  , SEQUENCE  , HEADS   , _
		stride_qb, stride_qm, stride_qh, _ = get_strides(query.shape)
		stride_kb, stride_kn, stride_kh, _ = get_strides(key.shape)
		stride_vb, stride_vn, stride_vh, _ = get_strides(value.shape)
		stride_ob, stride_om, stride_oh, _ = get_strides(o.shape)

		# BATCH  , HEADS    , _
		stride_lb, stride_lh, _ = get_strides(l.shape)
		stride_deb, stride_deh, _ = get_strides(delta.shape)

		# BATCH   , SEQUENCE  , HEADS     , _
		stride_dqb, stride_dqm, stride_dqh, _ = get_strides(query.shape)
		stride_dkb, stride_dkn, stride_dkh, _ = get_strides(key.shape)
		stride_dvb, stride_dvn, stride_dvh, _ = get_strides(value.shape)
		stride_dob, stride_dom, stride_doh, _ = get_strides(Do.shape)

		num_warps = 4 if headdim <= 64 else 8

		# kernel kwargs
		metaparams = dict(
			BLOCK_M=blocksize_q,
			BLOCK_HEADDIM=BLOCK_HEADDIM,
			num_warps=num_warps,
			num_stages=1,
		)
		(delta,) = triton_call(
			o,
			Do,
			delta,
			stride_ob,
			stride_om,
			stride_oh,
			stride_dob,
			stride_dom,
			stride_doh,
			stride_deb,
			stride_deh,
			nheads,
			headdim,
			seqlen_q,
			out_shape=[
				jax.ShapeDtypeStruct(
					shape=delta.shape,
					dtype=delta.dtype,
					sharding=get_sharding(delta),
				)
			],
			input_output_aliases={2: 0},
			grid=lambda META: (triton.cdiv(seqlen_q, META["BLOCK_M"]), batch * nheads, 1),
			kernel=_bwd_do_attn_kernel,
			name="triton::ops::_bwd_do_attn_kernel",
			**metaparams,
		)
		metaparams = dict(
			BLOCK_M=blocksize_q,
			BLOCK_N=blocksize_k,
			num_warps=num_warps,
			num_stages=1,
			BLOCK_HEADDIM=BLOCK_HEADDIM,
			HAVE_BIAS=HAVE_BIAS,
			BIAS_SINGLE_HEAD=BIAS_SINGLE_HEAD,
		)

		Dq, Dk, Dv = triton_call(
			query,
			key,
			value,
			bias if bias is not None else jnp.zeros((1,), jnp.float16),
			Do,
			l,
			delta,
			softmax_scale,
			stride_qb,
			stride_qm,
			stride_qh,
			stride_kb,
			stride_kn,
			stride_kh,
			stride_vb,
			stride_vn,
			stride_vh,
			stride_bb,
			stride_bh,
			stride_bm,
			stride_dob,
			stride_dom,
			stride_doh,
			stride_dqb,
			stride_dqm,
			stride_dqh,
			stride_dkb,
			stride_dkn,
			stride_dkh,
			stride_dvb,
			stride_dvn,
			stride_dvh,
			stride_lb,
			stride_lh,
			seqlen_q,
			seqlen_k,
			headdim,
			nheads,
			kernel=_bwd_attn_kernel,
			grid=lambda META: (triton.cdiv(seqlen_k, META["BLOCK_N"]), 1, batch * nheads),
			out_shape=bwd_kernel_out_shapes,
			name="triton::ops::_bwd_attn_kernel",
			**metaparams,
		)

		return Dq, Dk, Dv, None
	else:
		_, f_vjp = jax.vjp(
			functools.partial(_simp_attn, softmax_scale=softmax_scale),
			query,
			key,
			value,
			bias,
		)
		return f_vjp(Do)


def _fwd_attn_kernel_call_with_residual(
	query: Optional[chex.Array],
	key: Optional[chex.Array],
	value: Optional[chex.Array],
	bias: Optional[chex.Array] = None,
	softmax_scale: Optional[float] = None,
	blocksize_q: int = 128,
	blocksize_k: int = 128,
):
	"""Calls the Triton kernel for the forward pass of the attention mechanism and returns the residual.

	Args:
		query: Query array.
		key: Key array.
		value: Value array.
		bias: Bias array.
		softmax_scale: Scaling factor for the softmax function.
		blocksize_q: Block size for the query sequence dimension.
		blocksize_k: Block size for the key sequence dimension.

	Returns:
		Tuple of the output array and the residual.
	"""
	o, l = _fwd_attn_kernel_call(
		query=query,
		key=key,
		value=value,
		bias=bias,
		softmax_scale=softmax_scale,
		blocksize_k=blocksize_k,
		blocksize_q=blocksize_q,
	)
	return o, (o, l, query, key, value, bias)


@functools.partial(custom_vjp, nondiff_argnums=[4, 5, 6])
@functools.partial(jax.jit, static_argnums=[4, 5, 6])
def _flash_attn2(
	query: chex.Array,
	key: chex.Array,
	value: chex.Array,
	bias: Optional[chex.Array] = None,
	softmax_scale: Optional[float] = None,
	blocksize_q: int = 128,
	blocksize_k: int = 128,
) -> chex.Array:
	"""Computes the attention mechanism using the Triton kernel.

	Args:
		query: Query array of shape (batch, seq_len_q, num_heads, head_dim).
		key: Key array of shape (batch, seq_len_k, num_heads, head_dim).
		value: Value array of shape (batch, seq_len_k, num_heads, head_dim).
		bias: Optional bias array of shape (batch, num_heads, seq_len_q, seq_len_k).
		softmax_scale: Scaling factor for the softmax function.
		blocksize_q: Block size for the query sequence dimension.
		blocksize_k: Block size for the key sequence dimension.

	Returns:
		Output array of shape (batch, seq_len_q, num_heads, head_dim).
	"""
	return _fwd_attn_kernel_call(
		query=query,
		key=key,
		value=value,
		bias=bias,
		softmax_scale=softmax_scale,
		blocksize_k=blocksize_k,
		blocksize_q=blocksize_q,
	)[0]


_flash_attn2.defvjp(
	_fwd_attn_kernel_call_with_residual,
	_bwd_attn_kernel_call,
)
triton_flash_mha_attn_2_gpu = _flash_attn2
__all__ = ["triton_flash_mha_attn_2_gpu"]


def _attn_refrence(query_states, key_states, value_states, bias):
	b, qs, num_q_heads, d = query_states.shape
	num_kv_heads = value_states.shape[2]
	ks = value_states.shape[1]
	query_states = jnp.reshape(
		query_states,
		(b, qs, num_kv_heads, num_q_heads // num_kv_heads, d),
	)

	query_states = query_states * (d**-0.5)
	attention_weight = jnp.einsum(
		"bskhd,bmkd->bkhsm",
		query_states,
		key_states,
	)

	if bias is not None:
		if bias.shape[1] == num_q_heads:
			attention_weight = jnp.add(
				attention_weight,
				bias.reshape(b, num_kv_heads, num_q_heads // num_kv_heads, qs, ks),
			)
		elif bias.shape[1] == num_kv_heads:
			attention_weight = jnp.add(
				attention_weight,
				bias.reshape(b, num_kv_heads, 1, qs, ks),
			)
		elif bias.shape[1] == 1:
			attention_weight = jnp.add(
				attention_weight,
				bias.reshape(b, 1, 1, qs, ks),
			)
		else:
			raise NotImplementedError("bias heads wont match!")

	attention_weight = jax.nn.softmax(attention_weight)

	return jnp.einsum("bkhsm,bmkd->bskhd", attention_weight, value_states).reshape(
		b,
		qs,
		num_q_heads,
		d,
	)


def _test_forward():
	"""Tests the forward pass of the attention mechanism."""
	q_key, k_key, v_key = jrnd.split(jrnd.PRNGKey(8), 3)
	q_key, k_key, v_key = jrnd.split(jrnd.PRNGKey(8), 3)
	B, QH, KVH, QS, KS, D = 1, 32, 32, 1024, 1024, 128
	blocksize_k = 64
	blocksize_q = 128
	q = jax.nn.initializers.normal(2)(q_key, (B, QS, QH, D), dtype=jnp.float16)
	k = jax.nn.initializers.normal(2)(k_key, (B, KS, KVH, D), dtype=jnp.float16)
	v = jax.nn.initializers.normal(2)(v_key, (B, KS, KVH, D), dtype=jnp.float16)
	b = (
		jnp.where(
			jrnd.randint(v_key, (B, 1, QS, KS), 0, 4) > 2,
			jnp.finfo(jnp.float16).min,
			0,
		)
		if True
		else None
	)
	print("QKV Allocated")
	co = triton_flash_mha_attn_2_gpu(
		q,
		k,
		v,
		b,
		blocksize_q=blocksize_q,
		blocksize_k=blocksize_k,
	)
	print(co[-1, -1, -1, :5])
	fo = _attn_refrence(q, k, v, b)
	print(fo[-1, -1, -1, :5])
	print("Results are Close" if jnp.allclose(co, fo, 0, 0.125) else "Wrong results!")


def _test_backward():
	"""Tests the backward pass of the attention mechanism."""
	q_key, k_key, v_key = jrnd.split(jrnd.PRNGKey(8), 3)
	B, QH, KVH, QS, KS, D = 1, 32, 32, 1024, 1024, 128
	blocksize_k = 16
	blocksize_q = 16
	q = jax.nn.initializers.normal(2)(q_key, (B, QS, QH, D), dtype=jnp.float16)
	k = jax.nn.initializers.normal(2)(k_key, (B, KS, KVH, D), dtype=jnp.float16)
	v = jax.nn.initializers.normal(2)(v_key, (B, KS, KVH, D), dtype=jnp.float16)
	b = (
		jnp.where(
			jrnd.randint(v_key, (B, 1, QS, KS), 0, 4) > 2,
			jnp.finfo(jnp.float16).min,
			0,
		)
		if True
		else None
	)

	try:
		co = jax.grad(
			lambda *x: triton_flash_mha_attn_2_gpu(
				*x,
				blocksize_q=blocksize_q,
				blocksize_k=blocksize_k,
			).sum()
		)(q, k, v, b)
		print("Custom op backward pass gradients:")
		print(co[-1][-1, -1, :5])  # Print last 5 elements of last head of last batch
	except Exception as er:
		print(f"Custom op backward pass failed: {er}")
		co = None

	try:
		fo = jax.grad(lambda *x: _attn_refrence(*x).sum())(q, k, v, b)

		print(fo[-1, -1, -1, :5])  # Print last 5 elements of last head of last batch
	except Exception as e:
		print(f"Flax backward pass failed : {e}")
		fo = None
		exit()

	if fo is not None and co is not None:
		if jnp.allclose(co, fo, atol=0.125):
			print("Backward pass results are close.")
		else:
			print("Backward pass results differ significantly!")


if __name__ == "__main__":
	_test_forward()
	_test_backward()
