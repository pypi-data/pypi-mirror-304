from _heapq import *
from _typeshed import SupportsRichComparison
from collections.abc import Callable, Iterable
from typing import Any, Final, TypeVar

__all__ = ["heappush", "heappop", "heapify", "heapreplace", "merge", "nlargest", "nsmallest", "heappushpop"]

_S = TypeVar("_S")

__about__: Final[str]

def merge(
    *iterables: Iterable[_S], key: Callable[[_S], SupportsRichComparison] | None = None, reverse: bool = False
) -> Iterable[_S]: ...
def nlargest(n: int, iterable: Iterable[_S], key: Callable[[_S], SupportsRichComparison] | None = None) -> list[_S]: ...
def nsmallest(n: int, iterable: Iterable[_S], key: Callable[[_S], SupportsRichComparison] | None = None) -> list[_S]: ...
def _heapify_max(heap: list[Any], /) -> None:
    """Maxheap variant of heapify."""
    ...
