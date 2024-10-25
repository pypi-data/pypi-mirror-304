from typing import Callable, ParamSpec, TypeVar


T = TypeVar("T")
P = ParamSpec("P")
R = TypeVar("R")
C = Callable[P, T]


def copy_doc(source):
    """Copy the docstring from the source function to the decorated function."""

    def inner(func):
        return func

    return inner
