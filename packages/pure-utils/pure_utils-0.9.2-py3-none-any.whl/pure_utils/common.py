"""The common purpose utilities."""

from typing import TypeVar

__all__ = ["Singleton"]


T = TypeVar("T", bound="Singleton")


class Singleton(type):
    """A metaclass, implements the singleton pattern for inheritors.

    Usage:

    >>> from pure_utils import Singleton

    >>> class SomeSigletonClass(metaclass=Singleton):
    ...     pass
    >>> some = SomeSigletonClass()
    """

    _instances: dict = {}

    def __call__(cls: T, *args, **kwargs) -> T:
        """Get or create (first call) singleton object."""
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
