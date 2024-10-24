import sys
from _typeshed import SupportsItems
from collections.abc import Iterable
from typing import Any, Generic, TypeVar, overload

__all__ = ["TopologicalSorter", "CycleError"]

_T = TypeVar("_T")

if sys.version_info >= (3, 11):
    from types import GenericAlias

class TopologicalSorter(Generic[_T]):
    @overload
    def __init__(self, graph: None = None) -> None: ...
    @overload
    def __init__(self, graph: SupportsItems[_T, Iterable[_T]]) -> None: ...
    def add(self, node: _T, *predecessors: _T) -> None: ...
    def prepare(self) -> None: ...
    def is_active(self) -> bool: ...
    def __bool__(self) -> bool: ...
    def done(self, *nodes: _T) -> None: ...
    def get_ready(self) -> tuple[_T, ...]: ...
    def static_order(self) -> Iterable[_T]: ...
    if sys.version_info >= (3, 11):
        def __class_getitem__(cls, item: Any, /) -> GenericAlias:
            """
            Represent a PEP 585 generic type

            E.g. for t = list[int], t.__origin__ is list and t.__args__ is (int,).
            """
            ...

class CycleError(ValueError): ...
