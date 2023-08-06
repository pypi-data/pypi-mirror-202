from typing import Optional, Union

import jax.numpy as jnp
import jax.random as jrand
from equinox import filter_grad, filter_jit, filter_vmap
from jax._src.random import KeyArray, Shape
from jaxtyping import ArrayLike, Float

from ..core import make_partial_pipe
from ..math.special import fdtr, fdtri


@filter_jit
def _pf(
    x: Union[Float, ArrayLike],
    dfn: Union[Float, ArrayLike],
    dfd: Union[Float, ArrayLike],
):
    return fdtr(dfn, dfd, x)


@make_partial_pipe
def pF(
    q: Union[Float, ArrayLike],
    dfn: Union[Float, ArrayLike],
    dfd: Union[Float, ArrayLike],
    lower_tail: bool = True,
    log_prob: bool = False,
    dtype=jnp.float32,
) -> ArrayLike:
    """Calculates the cumulative distribution function of the F-distribution.

    Args:
        q (Union[Float, ArrayLike]): The value at which to evaluate the cdf.
        dfn (Union[Float, ArrayLike]): The numerator degrees of freedom.
        dfd (Union[Float, ArrayLike]): The denominator degrees of freedom.
        lower_tail (bool, optional): If True (default), the lower tail probability is returned.
        log_prob (bool, optional): If True, the logarithm of the probability is returned.
        dtype (jnp.dtype, optional): The dtype of the output (default is float32).

    Returns:
        ArrayLike: The cumulative distribution function evaluated at `q`.

    Example:
        >>> pF(1.0, 1.0, 1.0)
        Array([0.5000001], dtype=float32, weak_type=True)
    """
    q = jnp.asarray(q, dtype=dtype)
    q = jnp.atleast_1d(q)
    p = filter_vmap(_pf)(q, dfn, dfd)
    if not lower_tail:
        p = 1 - p
    if log_prob:
        p = jnp.log(p)
    return p


_df = filter_jit(filter_grad(_pf))


@make_partial_pipe
def dF(
    x: Union[Float, ArrayLike],
    dfn: Union[Float, ArrayLike],
    dfd: Union[Float, ArrayLike],
    lower_tail: bool = True,
    log_prob: bool = False,
    dtype=jnp.float32,
) -> ArrayLike:
    """Calculates the gradient of the cumulative distribution function for a given x, dfn and dfd.

    Args:
        x (Union[Float, ArrayLike]): The value at which to calculate the gradient of the cumulative distribution function.
        dfn (Union[Float, ArrayLike]): The numerator degrees of freedom.
        dfd (Union[Float, ArrayLike]): The denominator degrees of freedom.
        lower_tail (bool, optional): Whether to calculate the lower tail of the cumulative distribution function. Defaults to True.
        log_prob (bool, optional): Whether to return the log probability. Defaults to False.
        dtype (jnp.dtype, optional): The dtype of the output. Defaults to float32.

    Returns:
        ArrayLike: The gradient of the cumulative distribution function.

    Example:
        >>> dF(1.0, 1.0, 1.0)
        Array([0.1591549], dtype=float32, weak_type=True)
    """
    x = jnp.asarray(x, dtype=dtype)
    x = jnp.atleast_1d(x)
    grads = filter_vmap(_df)(x, dfn, dfd)
    if not lower_tail:
        grads = 1 - grads
    if log_prob:
        grads = jnp.log(grads)
    return grads


@filter_jit
def _qf(
    q: Union[Float, ArrayLike],
    dfn: Union[Float, ArrayLike],
    dfd: Union[Float, ArrayLike],
):
    return fdtri(dfn, dfd, q)


@make_partial_pipe
def qF(
    p: Union[Float, ArrayLike],
    dfn: Union[Float, ArrayLike],
    dfd: Union[Float, ArrayLike],
    lower_tail: bool = True,
    log_prob: bool = False,
    dtype=jnp.float32,
) -> ArrayLike:
    """Calculates the quantile function of a given distribution.

    Args:
        p (Union[Float, ArrayLike]): The quantile to calculate.
        dfn (Union[Float, ArrayLike]): The degrees of freedom for the numerator.
        dfd (Union[Float, ArrayLike]): The degrees of freedom for the denominator.
        lower_tail (bool, optional): Whether to calculate the lower tail or not. Defaults to True.
        log_prob (bool, optional): Whether to calculate the log probability or not. Defaults to False.

    Returns:
        ArrayLike: The calculated quantile.

    Example:
        >>> qF(0.5, 1.0, 1.0)
        Array([0.99999714], dtype=float32)
    """
    p = jnp.asarray(p, dtype=dtype)
    p = jnp.atleast_1d(p)
    if not lower_tail:
        p = 1 - p
    if log_prob:
        p = jnp.exp(p)
    return filter_vmap(_qf)(p, dfn, dfd)


@filter_jit
def _rf(
    key: KeyArray,
    dfn: Union[Float, ArrayLike],
    dfd: Union[Float, ArrayLike],
    sample_shape: Optional[Shape] = None,
    dtype = jnp.float32,
):
    if sample_shape is None:
        sample_shape = jnp.broadcast_shapes(jnp.shape(dfn), jnp.shape(dfd))
    dfn = jnp.broadcast_to(dfn, sample_shape)
    dfd = jnp.broadcast_to(dfd, sample_shape)
    return jrand.f(key, dfn, dfd, shape=sample_shape, dtype=dtype)


@make_partial_pipe
def rF(
    key: KeyArray,
    sample_shape: Optional[Shape] = None,
    dfn: Union[Float, ArrayLike] = None,
    dfd: Union[Float, ArrayLike] = None,
    lower_tail: bool = True,
    log_prob: bool = False,
    dtype = jnp.float32,
):
    """Generate random variates from F-distribution.

    Args:
        key (KeyArray): Random key used for PRNG.
        sample_shape (Optional[Shape], optional): Shape of the samples to be drawn. Defaults to None.
        dfn (Union[Float, ArrayLike]): Degrees of freedom in numerator.
        dfd (Union[Float, ArrayLike]): Degrees of freedom in denominator.
        lower_tail (bool, optional): Whether to calculate the lower tail probability. Defaults to True.
        log_prob (bool, optional): Whether to return the log probability. Defaults to False.
        dtype (jnp.dtype, optional): The dtype of the output. Defaults to float32.

    Returns:
        ArrayLike : Random variates from F-distribution.

    Example:
        >>> rF(jax.random.PRNGKey(0), dfn=1.0, dfd=1.0)
        Array(40.787617, dtype=float32)

    """
    rvs = _rf(key, dfn, dfd, sample_shape, dtype=dtype)
    if not lower_tail:
        rvs = 1 - rvs
    if log_prob:
        rvs = jnp.log(rvs)
    return rvs
