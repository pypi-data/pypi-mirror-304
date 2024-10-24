from collections.abc import Callable, Iterable, Mapping
from typing import Any

__all__ = ["BaseProcess", "current_process", "active_children", "parent_process"]

class BaseProcess:
    name: str
    daemon: bool
    authkey: bytes
    _identity: tuple[int, ...]  # undocumented
    def __init__(
        self,
        group: None = None,
        target: Callable[..., object] | None = None,
        name: str | None = None,
        args: Iterable[Any] = (),
        kwargs: Mapping[str, Any] = {},
        *,
        daemon: bool | None = None,
    ) -> None: ...
    def run(self) -> None: ...
    def start(self) -> None: ...
    def terminate(self) -> None: ...
    def kill(self) -> None: ...
    def close(self) -> None: ...
    def join(self, timeout: float | None = None) -> None: ...
    def is_alive(self) -> bool: ...
    @property
    def exitcode(self) -> int | None:
        """Return exit code of process or `None` if it has yet to stop"""
        ...
    @property
    def ident(self) -> int | None:
        """Return identifier (PID) of process or `None` if it has yet to start"""
        ...
    @property
    def pid(self) -> int | None:
        """Return identifier (PID) of process or `None` if it has yet to start"""
        ...
    @property
    def sentinel(self) -> int:
        """
        Return a file descriptor (Unix) or handle (Windows) suitable for
        waiting for process termination.
        """
        ...

def current_process() -> BaseProcess: ...
def active_children() -> list[BaseProcess]: ...
def parent_process() -> BaseProcess | None: ...
