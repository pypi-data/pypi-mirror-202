#!/usr/bin/env python
# -*- coding: utf-8 -*-

r"""Python ♡ Nasy.

    |             *         *
    |                  .                .
    |           .                              登
    |     *                      ,
    |                   .                      至
    |
    |                               *          恖
    |          |\___/|
    |          )    -(             .           聖 ·
    |         =\ -   /=
    |           )===(       *
    |          /   - \
    |          |-    |
    |         /   -   \     0.|.0
    |  NASY___\__( (__/_____(\=/)__+1s____________
    |  ______|____) )______|______|______|______|_
    |  ___|______( (____|______|______|______|____
    |  ______|____\_|______|______|______|______|_
    |  ___|______|______|______|______|______|____
    |  ______|______|______|______|______|______|_
    |  ___|______|______|______|______|______|____

author   : Nasy https://nasy.moe
date     : Apr  7, 2023
email    : Nasy <nasyxx+python@gmail.com>
filename : basic.py
project  : jaxrie
license  : GPL-3.0+

Basic
"""

# Types
from typing import Callable
from jax.typing import ArrayLike

# JAX
import haiku as hk
import jax
import jax.numpy as jnp

# Local
from jaxrie.manifold import Manifold

Array = jax.Array


class HAct(hk.Module):
  """Hyperbolic Activation Layer."""

  def __init__(
      self,
      activation: Callable[[Array], Array],
      manifold: Manifold,
      cin: ArrayLike | None = None,
      cout: ArrayLike | None = None,
      name: str | None = None,
  ) -> None:
    """Initialize the layer."""
    super().__init__(name=name)
    self.m = manifold
    self.activation = activation

    self.tcin = cin is None
    self.tcout = cout is None
    self.cin = -1.0 if self.tcin else cin
    self.cout = -1.0 if self.tcout else cout

  def __call__(self, x: Array) -> Array:
    """Apply the layer."""
    dtype = x.dtype
    self.cin = jnp.array(self.cin, dtype=dtype)
    self.cout = jnp.array(self.cout, dtype=dtype)
    if self.tcin:
      self.cin = hk.get_parameter("cin", (), init=hk.initializers.Constant(self.cin))
    if self.tcout:
      self.cout = hk.get_parameter("cout", (), init=hk.initializers.Constant(self.cout))

    return self.m.proj(
        self.m.expmap0(self.activation(self.m.logmap0(x, self.cin)), self.cout),
        self.cout,
    )


class HLinear(hk.Module):
  """Hyperbolic Linear Layer."""

  def __init__(
      self,
      out_features: int,
      manifold: Manifold,
      c: ArrayLike | None = None,
      with_bias: bool = True,
      w_init: hk.initializers.Initializer | None = None,
      b_init: hk.initializers.Initializer | None = None,
      name: str | None = None,
  ) -> None:
    """Initialize the layer."""
    super().__init__(name=name)
    self.out_features = out_features
    self.m = manifold

    self.tc = c is None
    self.c = -1.0 if c is None else c
    self.w_init = w_init
    self.b_init = b_init or hk.initializers.Constant(0.0)
    self.with_bias = with_bias

  def __call__(self, x: Array) -> Array:
    """Apply the layer."""
    dtype = x.dtype
    input_size = self.input_size = x.shape[-1]
    w_init = self.w_init

    self.c = jnp.array(self.c, dtype=dtype)
    if self.tc:
      self.c = hk.get_parameter("c", (), init=hk.initializers.Constant(self.c))

    if w_init is None:
      stddev = 1.0 / jnp.sqrt(input_size)
      w_init = hk.initializers.TruncatedNormal(stddev=stddev)
    w = hk.get_parameter("w", [input_size, self.out_features], dtype, init=w_init)

    out = self.m.proj(self.m.matmull(x, w, self.c), self.c)

    if self.with_bias:
      b = hk.get_parameter("b", [self.out_features], dtype, init=self.b_init)
      out = self.m.proj(self.m.adde(out, b, self.c), self.c)

    return out


class HGCN(hk.Module):
  """Hyperbolic Graph Convolutional Network."""

  def __init__(
      self,
      out_features: int,
      manifold: Manifold,
      c: ArrayLike | None = None,
      with_bias: bool = True,
      w_init: hk.initializers.Initializer | None = None,
      b_init: hk.initializers.Initializer | None = None,
      name: str | None = None,
  ) -> None:
    """Initialize the layer."""
    super().__init__(name=name)
    self.out_features = out_features
    self.m = manifold

    self.tc = c is None
    self.c = -1.0 if c is None else c
    self.with_bias = with_bias

    w_init = w_init or hk.initializers.VarianceScaling(1.0, "fan_avg", "uniform")

    self.linear = HLinear(
        out_features,
        manifold,
        c=c,
        with_bias=with_bias,
        w_init=w_init,
        b_init=b_init,
        name="hlinear",
    )

  def __call__(self, x: Array, adj: Array) -> Array:
    """Apply the layer."""
    out = self.linear(x)
    self.c = self.linear.c
    return self.m.proj(self.m.matmulr(adj, out, self.c), self.c)
