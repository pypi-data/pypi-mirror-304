from collections.abc import Callable, Mapping
from typing import Any, Generic, TypeVar, overload

_T = TypeVar("_T")
_S = TypeVar("_S")

class _SingleDispatchCallable(Generic[_T]):
    registry: Mapping[Any, Callable[..., _T]]
    def dispatch(self, cls: Any) -> Callable[..., _T]: ...
    @overload
    def register(self, cls: Any) -> Callable[[Callable[..., _T]], Callable[..., _T]]: ...
    @overload
    def register(self, cls: Any, func: Callable[..., _T]) -> Callable[..., _T]: ...
    def _clear_cache(self) -> None: ...
    def __call__(self, *args: Any, **kwargs: Any) -> _T: ...

def singledispatch(func: Callable[..., _T]) -> _SingleDispatchCallable[_T]: ...

class singledispatchmethod(Generic[_T]):
    dispatcher: _SingleDispatchCallable[_T]
    func: Callable[..., _T]
    def __init__(self, func: Callable[..., _T]) -> None: ...
    @property
    def __isabstractmethod__(self) -> bool: ...
    @overload
    def register(self, cls: type[Any], method: None = ...) -> Callable[[Callable[..., _T]], Callable[..., _T]]: ...
    @overload
    def register(self, cls: Callable[..., _T], method: None = ...) -> Callable[..., _T]: ...
    @overload
    def register(self, cls: type[Any], method: Callable[..., _T]) -> Callable[..., _T]: ...
    def __get__(self, obj: _S, cls: type[_S] | None = ...) -> Callable[..., _T]: ...
