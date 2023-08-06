from functools import partial, wraps
from typing import Callable, Hashable, ParamSpec, TypeVar

from equinox import filter_pmap, filter_vmap

from .base import Functional


P = ParamSpec("P")
T = TypeVar("T")


def pipe_vmap(
    func: Callable[P, T] = None,
    *,
    in_axes=0,
    out_axes=0,
    axis_name: Hashable = None,
    axis_size: int | None = None,
    name: str = None
) -> Callable[P, T]:
    """Creates a functional from a function with vmap.

    Args:
        func: The function to be wrapped.
        in_axes: The number of input axes.
        out_axes: The number of output axes.
        axis_name: The name of the axis.
        axis_size: The size of the axis.
        name: The name of the functional. If not provided, the name of the
        function is used.

    Returns:
        A callable that creates a functional from the given function.

    Example:
        >>> from stamox.core import pipe_vmap
        >>> f = lambda x: x + 1
        >>> f = pipe_vmap(f)
        >>> g = f >> f >> f
        >>> g(jnp.array([1, 2, 3]))
        Array([4, 5, 6], dtype=int32)
    """
    if name is None and func is not None:
        if hasattr(func, "name"):
            name = func.name
        else:
            name = func.__name__

    @wraps(func)
    def wrap(func: Callable[P, T]) -> Callable:
        if isinstance(func, Functional):
            func = func.func
        fn = filter_vmap(
            func,
            in_axes=in_axes,
            out_axes=out_axes,
            axis_name=axis_name,
            axis_size=axis_size,
        )
        return Functional(name=name, fn=fn)

    return wrap if func is None else wrap(func)


def partial_pipe_vmap(
    func: Callable[P, T] = None, *, name: str = None
) -> Callable[P, T]:
    """Partially apply a function to a vmap.

    Args:
        func (Callable[P, T]): The function to partially apply.
        name (str, optional): The name of the function. Defaults to None.

    Returns:
        Callable[P, T]: A partially applied function.

    Example:
        >>> from stamox.core import partial_pipe_vmap
        >>> f = lambda x, y: x + y
        >>> f = partial_pipe_vmap(f)
        >>> g = f(y=1) >> f(y=2) >> f(y=3)
        >>> g(jnp.array([1, 2, 3]))
        Array([7, 8, 9], dtype=int32)
    """
    if name is None and func is not None:
        if hasattr(func, "name"):
            name = func.name
        else:
            name = func.__name__

    @wraps(func)
    def wrap(func: Callable[P, T]) -> Callable:
        if isinstance(func, Functional):
            func = func.func

        @wraps(func)
        def partial_fn(
            *args,
            in_axes=0,
            out_axes=0,
            axis_name: Hashable = None,
            axis_size: int | None = None,
            **kwargs
        ):
            fn = partial(func, **kwargs)
            fn = filter_vmap(
                fn,
                in_axes=in_axes,
                out_axes=out_axes,
                axis_name=axis_name,
                axis_size=axis_size,
            )
            if len(args) != 0:
                return fn(*args)
            return Functional(name=name, fn=fn)

        return partial_fn

    return wrap if func is None else wrap(func)


def pipe_pmap(
    func: Callable[P, T] = None,
    *,
    in_axes=0,
    out_axes=0,
    axis_name: Hashable = None,
    axis_size: int | None = None,
    name: str = None
) -> Callable[P, T]:
    """Creates a functional object from a given function.

    Args:
        func (Callable[P, T]): The function to be wrapped.
        in_axes (int): The number of input axes for the function.
        out_axes (int): The number of output axes for the function.
        axis_name (Hashable): The name of the axis.
        axis_size (int | None): The size of the axis.
        name (str): The name of the functional object.

    Returns:
        Callable[P, T]: A callable object that wraps the given function.

    Example:
        >>> from stamox.core import pipe_pmap
        >>> f = lambda x: x + 1
        >>> f = pipe_pmap(f)
        >>> g = f >> f >> f
        >>> g(jnp.array([1, 2, 3]))
        Array([4, 5, 6], dtype=int32)
    """
    if name is None and func is not None:
        if hasattr(func, "name"):
            name = func.name
        else:
            name = func.__name__

    @wraps(func)
    def wrap(func: Callable[P, T]) -> Callable:
        if isinstance(func, Functional):
            func = func.func
        fn = filter_pmap(
            func,
            in_axes=in_axes,
            out_axes=out_axes,
            axis_name=axis_name,
            axis_size=axis_size,
        )

        return Functional(name=name, fn=fn)

    return wrap if func is None else wrap(func)


def partial_pipe_pmap(
    func: Callable[P, T] = None, *, name: str = None
) -> Callable[P, T]:
    """Partially apply a function to a pipe.

    Args:
        func (Callable[P, T]): The function to partially apply.
        name (str, optional): The name of the function. Defaults to None.

    Returns:
        Callable[P, T]: A partially applied function.

    Example:
        >>> from stamox.core import partial_pipe_pmap
        >>> f = lambda x, y: x + y
        >>> f = partial_pipe_pmap(f)
        >>> g = f(y=1) >> f(y=2) >> f(y=3)
        >>> g(jnp.array([1, 2, 3]))
        Array([7, 8, 9], dtype=int32)
    """
    if name is None and func is not None:
        if hasattr(func, "name"):
            name = func.name
        else:
            name = func.__name__

    @wraps(func)
    def wrap(func: Callable[P, T]) -> Callable:
        if isinstance(func, Functional):
            func = func.func

        @wraps(func)
        def partial_fn(
            *args,
            in_axes=0,
            out_axes=0,
            axis_name: Hashable = None,
            axis_size: int | None = None,
            **kwargs
        ):
            fn = partial(func, **kwargs)
            fn = filter_pmap(
                fn,
                in_axes=in_axes,
                out_axes=out_axes,
                axis_name=axis_name,
                axis_size=axis_size,
            )
            if len(args) != 0:
                return fn(*args, **kwargs)
            return Functional(name=name, fn=fn, is_partial=True)

        return partial_fn

    return wrap if func is None else wrap(func)
