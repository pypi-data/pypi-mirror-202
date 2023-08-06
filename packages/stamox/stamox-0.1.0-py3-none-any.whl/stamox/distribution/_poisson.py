from typing import Optional, Union

import jax.numpy as jnp
import jax.random as jrand
from equinox import filter_jit, filter_vmap
from jax._src.random import Shape
from jax.random import KeyArray
from jax.scipy.special import gammainc, gammaln
from jaxtyping import Array, ArrayLike, Bool, Float
from tensorflow_probability.substrates.jax.distributions.poisson import Poisson

from ..core import make_partial_pipe


@filter_jit
def _ppoisson(x: Union[Float, ArrayLike], rate: Union[Float, ArrayLike]) -> Array:
    k = jnp.floor(x) + 1.0
    return 1 - gammainc(k, rate)


@make_partial_pipe
def ppoisson(
    q: Union[Float, ArrayLike],
    rate: Union[Float, ArrayLike],
    lower_tail=True,
    log_prob=False,
) -> Array:
    """Computes the cumulative distribution function of the Poisson distribution.

    Args:
        q (Union[Float, ArrayLike]): The value at which to evaluate the CDF.
        rate (Union[Float, ArrayLike]): The rate parameter of the Poisson distribution.
        lower_tail (bool, optional): Whether to compute the lower tail of the CDF. Defaults to True.
        log_prob (bool, optional): Whether to return the log probability. Defaults to False.

    Returns:
        ArrayLike: The cumulative distribution function of the Poisson distribution evaluated at `q`.
    """
    q = jnp.asarray(q)
    q = jnp.atleast_1d(q)
    p = filter_vmap(_ppoisson)(q, rate)
    if not lower_tail:
        p = 1 - p
    if log_prob:
        p = jnp.log(p)
    return p


@filter_jit
def _dpoisson(x, rate):
    e = jnp.exp(-rate)
    numerator = rate**x
    denominator = jnp.exp(gammaln(x + 1))
    return (numerator / denominator) * e


@make_partial_pipe
def dpoisson(
    x: Union[Float, ArrayLike],
    rate: Union[Float, ArrayLike],
    lower_tail=True,
    log_prob=False,
) -> Array:
    """Computes the probability density function of the Poisson distribution.

    Args:
        x (Union[Float, ArrayLike]): The value at which to evaluate the PDF.
        rate (Union[Float, ArrayLike]): The rate parameter of the Poisson distribution.
        lower_tail (bool, optional): Whether to compute the lower tail of the PDF. Defaults to True.
        log_prob (bool, optional): Whether to return the log probability. Defaults to False.

    Returns:
        Array: The probability density function of the Poisson distribution evaluated at `x`.
    """
    x = jnp.asarray(x)
    x = jnp.atleast_1d(x)
    grads = filter_vmap(_dpoisson)(x, rate)
    if not lower_tail:
        grads = 1 - grads
    if log_prob:
        grads = jnp.log(grads)
    return grads


@filter_jit
def _rpoisson(
    key: KeyArray, rate: Union[Float, ArrayLike], sample_shape: Optional[Shape] = None
):
    return jrand.poisson(key, rate, shape=sample_shape)


@make_partial_pipe
def rpoisson(
    key: KeyArray,
    sample_shape: Optional[Shape] = None,
    rate: Union[Float, ArrayLike] = None,
    lower_tail=True,
    log_prob=False,
) -> Array:
    """Generates samples from the Poisson distribution.

    Args:
        key (KeyArray): Random number generator state used for random sampling.
        rate (Union[Float, ArrayLike]): The rate parameter of the Poisson distribution.
        sample_shape (Optional[Shape], optional): Shape of the output array. Defaults to None.
        lower_tail (bool, optional): Whether to return the lower tail probability. Defaults to True.
        log_prob (bool, optional): Whether to return the log probability. Defaults to False.

    Returns:
        Array: Samples from the Poisson distribution.
    """
    rvs = _rpoisson(key, rate, sample_shape=sample_shape)
    if not lower_tail:
        rvs = 1 - rvs
    if log_prob:
        rvs = jnp.log(rvs)
    return rvs


@filter_jit
def _qpoisson(q, rate):
    """
    Computes the p-th quantile of a Poisson distribution with mean rate use approximate
    """
    pass


    


@make_partial_pipe
def qpoisson(
    q: Union[Float, ArrayLike],
    rate: Union[Float, ArrayLike],
    lower_tail: Bool = True,
    log_prob: Bool = False,
) -> ArrayLike:
    """Computes the quantile function of the Poisson distribution.

    Args:
        q (Union[Float, ArrayLike]): The quantile at which to evaluate the quantile function.
        rate (Union[Float, ArrayLike]): The rate parameter of the Poisson distribution.

    Returns:
        Array: The quantile function of the Poisson distribution evaluated at `q`.
    """
    ImportWarning("qpoisson is not yet well tested.")
    raise NotImplementedError("Not Implemented Yet!")
    q = jnp.atleast_1d(q)
    if not lower_tail:
        q = 1 - q
    if log_prob:
        q = jnp.exp(q)
    return filter_vmap(_qpoisson)(q, rate)
