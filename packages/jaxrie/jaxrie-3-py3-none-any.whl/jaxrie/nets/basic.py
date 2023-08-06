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
date     : Apr 11, 2023
email    : Nasy <nasyxx+python@gmail.com>
filename : basic.py
project  : jaxrie
license  : GPL-3.0+

Nets
"""

# Standard Library
from collections.abc import Callable, Sequence

# JAX
import haiku as hk
import jax
from jax._src.basearray import ArrayLike

# Local
from jaxrie import HAct, HLinear, Manifold

Array = jax.Array


class HMLP(hk.Module):
  """A simple MLP."""

  def __init__(
      self,
      layers: Sequence[int],
      manifold: Manifold,
      activation: Callable[[Array], Array] = jax.nn.relu,
      c: ArrayLike | None = None,
      with_bias: bool = True,
      w_init: hk.initializers.Initializer | None = None,
      b_init: hk.initializers.Initializer | None = None,
      name: str | None = None,
  ) -> None:
    """Initialize the Hyperbolic MLP."""
    super().__init__(name=name)
    self.layers = list(
        map(lambda o: HLinear(o, manifold, c, with_bias, w_init, b_init), layers)
    )
    self.m = manifold
    self.activation = HAct(activation, manifold, c, c)
    self.tc = c is None
    self.c = -1.0 if self.tc else c

  def __call__(
      self, x: Array, dropout: float | None = None, train: bool = True
  ) -> Array:
    """Forward pass."""
    for layer in self.layers[:-1]:
      x = self.activation(layer(x))
      if train and dropout is not None:
        x = hk.dropout(hk.next_rng_key(), dropout, x)

    return self.layers[-1](x)
