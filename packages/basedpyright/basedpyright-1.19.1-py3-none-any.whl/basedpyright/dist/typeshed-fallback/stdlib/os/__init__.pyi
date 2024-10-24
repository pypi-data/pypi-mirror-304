import sys
from _typeshed import (
    AnyStr_co,
    BytesPath,
    FileDescriptor,
    FileDescriptorLike,
    FileDescriptorOrPath,
    GenericPath,
    OpenBinaryMode,
    OpenBinaryModeReading,
    OpenBinaryModeUpdating,
    OpenBinaryModeWriting,
    OpenTextMode,
    ReadableBuffer,
    StrOrBytesPath,
    StrPath,
    SupportsLenAndGetItem,
    Unused,
    WriteableBuffer,
    structseq,
)
from abc import abstractmethod
from builtins import OSError
from collections.abc import Callable, Iterable, Iterator, Mapping, MutableMapping, Sequence
from contextlib import AbstractContextManager
from io import BufferedRandom, BufferedReader, BufferedWriter, FileIO, TextIOWrapper
from subprocess import Popen
from types import TracebackType
from typing import (
    IO,
    Any,
    AnyStr,
    BinaryIO,
    Final,
    Generic,
    Literal,
    NoReturn,
    Protocol,
    TypeVar,
    final,
    overload,
    runtime_checkable,
)
from typing_extensions import Self, TypeAlias, Unpack, deprecated

from . import path as _path

if sys.version_info >= (3, 9):
    from types import GenericAlias

# This unnecessary alias is to work around various errors
path = _path

_T = TypeVar("_T")
_T1 = TypeVar("_T1")
_T2 = TypeVar("_T2")

# ----- os variables -----

error = OSError

supports_bytes_environ: bool

supports_dir_fd: set[Callable[..., Any]]
supports_fd: set[Callable[..., Any]]
supports_effective_ids: set[Callable[..., Any]]
supports_follow_symlinks: set[Callable[..., Any]]

if sys.platform != "win32":
    # Unix only
    PRIO_PROCESS: int
    PRIO_PGRP: int
    PRIO_USER: int

    F_LOCK: int
    F_TLOCK: int
    F_ULOCK: int
    F_TEST: int

    if sys.platform != "darwin":
        POSIX_FADV_NORMAL: int
        POSIX_FADV_SEQUENTIAL: int
        POSIX_FADV_RANDOM: int
        POSIX_FADV_NOREUSE: int
        POSIX_FADV_WILLNEED: int
        POSIX_FADV_DONTNEED: int

    if sys.platform != "linux" and sys.platform != "darwin":
        # In the os-module docs, these are marked as being available
        # on "Unix, not Emscripten, not WASI."
        # However, in the source code, a comment indicates they're "FreeBSD constants".
        # sys.platform could have one of many values on a FreeBSD Python build,
        # so the sys-module docs recommend doing `if sys.platform.startswith('freebsd')`
        # to detect FreeBSD builds. Unfortunately that would be too dynamic
        # for type checkers, however.
        SF_NODISKIO: int
        SF_MNOWAIT: int
        SF_SYNC: int

        if sys.version_info >= (3, 11):
            SF_NOCACHE: int

    if sys.platform == "linux":
        XATTR_SIZE_MAX: int
        XATTR_CREATE: int
        XATTR_REPLACE: int

    P_PID: int
    P_PGID: int
    P_ALL: int

    if sys.platform == "linux" and sys.version_info >= (3, 9):
        P_PIDFD: int

    WEXITED: int
    WSTOPPED: int
    WNOWAIT: int

    CLD_EXITED: int
    CLD_DUMPED: int
    CLD_TRAPPED: int
    CLD_CONTINUED: int

    if sys.version_info >= (3, 9):
        CLD_KILLED: int
        CLD_STOPPED: int

    # TODO: SCHED_RESET_ON_FORK not available on darwin?
    # TODO: SCHED_BATCH and SCHED_IDLE are linux only?
    SCHED_OTHER: int  # some flavors of Unix
    SCHED_BATCH: int  # some flavors of Unix
    SCHED_IDLE: int  # some flavors of Unix
    SCHED_SPORADIC: int  # some flavors of Unix
    SCHED_FIFO: int  # some flavors of Unix
    SCHED_RR: int  # some flavors of Unix
    SCHED_RESET_ON_FORK: int  # some flavors of Unix

if sys.platform != "win32":
    RTLD_LAZY: int
    RTLD_NOW: int
    RTLD_GLOBAL: int
    RTLD_LOCAL: int
    RTLD_NODELETE: int
    RTLD_NOLOAD: int

if sys.platform == "linux":
    RTLD_DEEPBIND: int
    GRND_NONBLOCK: int
    GRND_RANDOM: int

if sys.platform == "darwin" and sys.version_info >= (3, 12):
    PRIO_DARWIN_BG: int
    PRIO_DARWIN_NONUI: int
    PRIO_DARWIN_PROCESS: int
    PRIO_DARWIN_THREAD: int

SEEK_SET: int
SEEK_CUR: int
SEEK_END: int
if sys.platform != "win32":
    SEEK_DATA: int  # some flavors of Unix
    SEEK_HOLE: int  # some flavors of Unix

O_RDONLY: int
O_WRONLY: int
O_RDWR: int
O_APPEND: int
O_CREAT: int
O_EXCL: int
O_TRUNC: int
# We don't use sys.platform for O_* flags to denote platform-dependent APIs because some codes,
# including tests for mypy, use a more finer way than sys.platform before using these APIs
# See https://github.com/python/typeshed/pull/2286 for discussions
O_DSYNC: int  # Unix only
O_RSYNC: int  # Unix only
O_SYNC: int  # Unix only
O_NDELAY: int  # Unix only
O_NONBLOCK: int  # Unix only
O_NOCTTY: int  # Unix only
O_CLOEXEC: int  # Unix only
O_SHLOCK: int  # Unix only
O_EXLOCK: int  # Unix only
O_BINARY: int  # Windows only
O_NOINHERIT: int  # Windows only
O_SHORT_LIVED: int  # Windows only
O_TEMPORARY: int  # Windows only
O_RANDOM: int  # Windows only
O_SEQUENTIAL: int  # Windows only
O_TEXT: int  # Windows only
O_ASYNC: int  # Gnu extension if in C library
O_DIRECT: int  # Gnu extension if in C library
O_DIRECTORY: int  # Gnu extension if in C library
O_NOFOLLOW: int  # Gnu extension if in C library
O_NOATIME: int  # Gnu extension if in C library
O_PATH: int  # Gnu extension if in C library
O_TMPFILE: int  # Gnu extension if in C library
O_LARGEFILE: int  # Gnu extension if in C library
O_ACCMODE: int  # TODO: when does this exist?

if sys.platform != "win32" and sys.platform != "darwin":
    # posix, but apparently missing on macos
    ST_APPEND: int
    ST_MANDLOCK: int
    ST_NOATIME: int
    ST_NODEV: int
    ST_NODIRATIME: int
    ST_NOEXEC: int
    ST_RELATIME: int
    ST_SYNCHRONOUS: int
    ST_WRITE: int

if sys.platform != "win32":
    NGROUPS_MAX: int
    ST_NOSUID: int
    ST_RDONLY: int

curdir: str
pardir: str
sep: str
if sys.platform == "win32":
    altsep: str
else:
    altsep: str | None
extsep: str
pathsep: str
defpath: str
linesep: str
devnull: str
name: str

F_OK: int
R_OK: int
W_OK: int
X_OK: int

_EnvironCodeFunc: TypeAlias = Callable[[AnyStr], AnyStr]

class _Environ(MutableMapping[AnyStr, AnyStr], Generic[AnyStr]):
    encodekey: _EnvironCodeFunc[AnyStr]
    decodekey: _EnvironCodeFunc[AnyStr]
    encodevalue: _EnvironCodeFunc[AnyStr]
    decodevalue: _EnvironCodeFunc[AnyStr]
    if sys.version_info >= (3, 9):
        def __init__(
            self,
            data: MutableMapping[AnyStr, AnyStr],
            encodekey: _EnvironCodeFunc[AnyStr],
            decodekey: _EnvironCodeFunc[AnyStr],
            encodevalue: _EnvironCodeFunc[AnyStr],
            decodevalue: _EnvironCodeFunc[AnyStr],
        ) -> None: ...
    else:
        putenv: Callable[[AnyStr, AnyStr], object]
        unsetenv: Callable[[AnyStr, AnyStr], object]
        def __init__(
            self,
            data: MutableMapping[AnyStr, AnyStr],
            encodekey: _EnvironCodeFunc[AnyStr],
            decodekey: _EnvironCodeFunc[AnyStr],
            encodevalue: _EnvironCodeFunc[AnyStr],
            decodevalue: _EnvironCodeFunc[AnyStr],
            putenv: Callable[[AnyStr, AnyStr], object],
            unsetenv: Callable[[AnyStr, AnyStr], object],
        ) -> None: ...

    def setdefault(self, key: AnyStr, value: AnyStr) -> AnyStr: ...
    def copy(self) -> dict[AnyStr, AnyStr]: ...
    def __delitem__(self, key: AnyStr) -> None: ...
    def __getitem__(self, key: AnyStr) -> AnyStr: ...
    def __setitem__(self, key: AnyStr, value: AnyStr) -> None: ...
    def __iter__(self) -> Iterator[AnyStr]: ...
    def __len__(self) -> int: ...
    if sys.version_info >= (3, 9):
        def __or__(self, other: Mapping[_T1, _T2]) -> dict[AnyStr | _T1, AnyStr | _T2]: ...
        def __ror__(self, other: Mapping[_T1, _T2]) -> dict[AnyStr | _T1, AnyStr | _T2]: ...
        # We use @overload instead of a Union for reasons similar to those given for
        # overloading MutableMapping.update in stdlib/typing.pyi
        # The type: ignore is needed due to incompatible __or__/__ior__ signatures
        @overload  # type: ignore[misc]
        def __ior__(self, other: Mapping[AnyStr, AnyStr]) -> Self: ...
        @overload
        def __ior__(self, other: Iterable[tuple[AnyStr, AnyStr]]) -> Self: ...

environ: _Environ[str]
if sys.platform != "win32":
    environb: _Environ[bytes]

if sys.version_info >= (3, 11) or sys.platform != "win32":
    EX_OK: int

if sys.platform != "win32":
    confstr_names: dict[str, int]
    pathconf_names: dict[str, int]
    sysconf_names: dict[str, int]

    EX_USAGE: int
    EX_DATAERR: int
    EX_NOINPUT: int
    EX_NOUSER: int
    EX_NOHOST: int
    EX_UNAVAILABLE: int
    EX_SOFTWARE: int
    EX_OSERR: int
    EX_OSFILE: int
    EX_CANTCREAT: int
    EX_IOERR: int
    EX_TEMPFAIL: int
    EX_PROTOCOL: int
    EX_NOPERM: int
    EX_CONFIG: int

# Exists on some Unix platforms, e.g. Solaris.
if sys.platform != "win32" and sys.platform != "darwin" and sys.platform != "linux":
    EX_NOTFOUND: int

P_NOWAIT: int
P_NOWAITO: int
P_WAIT: int
if sys.platform == "win32":
    P_DETACH: int
    P_OVERLAY: int

# wait()/waitpid() options
if sys.platform != "win32":
    WNOHANG: int  # Unix only
    WCONTINUED: int  # some Unix systems
    WUNTRACED: int  # Unix only

TMP_MAX: int  # Undocumented, but used by tempfile

# ----- os classes (structures) -----
@final
class stat_result(structseq[float], tuple[int, int, int, int, int, int, int, float, float, float]):
    # The constructor of this class takes an iterable of variable length (though it must be at least 10).
    #
    # However, this class behaves like a tuple of 10 elements,
    # no matter how long the iterable supplied to the constructor is.
    # https://github.com/python/typeshed/pull/6560#discussion_r767162532
    #
    # The 10 elements always present are st_mode, st_ino, st_dev, st_nlink,
    # st_uid, st_gid, st_size, st_atime, st_mtime, st_ctime.
    #
    # More items may be added at the end by some implementations.
    if sys.version_info >= (3, 10):
        __match_args__: Final = ("st_mode", "st_ino", "st_dev", "st_nlink", "st_uid", "st_gid", "st_size")

    @property
    def st_mode(self) -> int:
        """protection bits"""
        ...
    @property
    def st_ino(self) -> int:
        """inode"""
        ...
    @property
    def st_dev(self) -> int:
        """device"""
        ...
    @property
    def st_nlink(self) -> int:
        """number of hard links"""
        ...
    @property
    def st_uid(self) -> int:
        """user ID of owner"""
        ...
    @property
    def st_gid(self) -> int:
        """group ID of owner"""
        ...
    @property
    def st_size(self) -> int:
        """total size, in bytes"""
        ...
    @property
    def st_atime(self) -> float:
        """time of last access"""
        ...
    @property
    def st_mtime(self) -> float:
        """time of last modification"""
        ...
    # platform dependent (time of most recent metadata change on Unix, or the time of creation on Windows)
    if sys.version_info >= (3, 12) and sys.platform == "win32":
        @property
        @deprecated(
            """\
Use st_birthtime instead to retrieve the file creation time. \
In the future, this property will contain the last metadata change time."""
        )
        def st_ctime(self) -> float: ...
    else:
        @property
        def st_ctime(self) -> float:
            """time of last change"""
            ...

    @property
    def st_atime_ns(self) -> int:
        """time of last access in nanoseconds"""
        ...
    @property
    def st_mtime_ns(self) -> int:
        """time of last modification in nanoseconds"""
        ...
    # platform dependent (time of most recent metadata change on Unix, or the time of creation on Windows) in nanoseconds
    @property
    def st_ctime_ns(self) -> int:
        """time of last change in nanoseconds"""
        ...
    if sys.platform == "win32":
        @property
        def st_file_attributes(self) -> int: ...
        @property
        def st_reparse_tag(self) -> int: ...
        if sys.version_info >= (3, 12):
            @property
            def st_birthtime(self) -> float: ...  # time of file creation in seconds
            @property
            def st_birthtime_ns(self) -> int: ...  # time of file creation in nanoseconds
    else:
        @property
        def st_blocks(self) -> int:
            """number of blocks allocated"""
            ...
        @property
        def st_blksize(self) -> int:
            """blocksize for filesystem I/O"""
            ...
        @property
        def st_rdev(self) -> int:
            """device type (if inode device)"""
            ...
        if sys.platform != "linux":
            # These properties are available on MacOS, but not Ubuntu.
            # On other Unix systems (such as FreeBSD), the following attributes may be
            # available (but may be only filled out if root tries to use them):
            @property
            def st_gen(self) -> int:
                """generation number"""
                ...
            @property
            def st_birthtime(self) -> float:
                """time of creation"""
                ...
    if sys.platform == "darwin":
        @property
        def st_flags(self) -> int: ...  # user defined flags for file
    # Attributes documented as sometimes appearing, but deliberately omitted from the stub: `st_creator`, `st_rsize`, `st_type`.
    # See https://github.com/python/typeshed/pull/6560#issuecomment-991253327

@runtime_checkable
class PathLike(Protocol[AnyStr_co]):
    @abstractmethod
    def __fspath__(self) -> AnyStr_co: ...

@overload
def listdir(path: StrPath | None = None) -> list[str]:
    r"""
    Return a list containing the names of the files in the directory.

    path can be specified as either str, bytes, or a path-like object.  If path is bytes,
      the filenames returned will also be bytes; in all other circumstances
      the filenames returned will be str.
    If path is None, uses the path='.'.
    On some platforms, path may also be specified as an open file descriptor;\
      the file descriptor must refer to a directory.
      If this functionality is unavailable, using it raises NotImplementedError.

    The list is in arbitrary order.  It does not include the special
    entries '.' and '..' even if they are present in the directory.
    """
    ...
@overload
def listdir(path: BytesPath) -> list[bytes]:
    r"""
    Return a list containing the names of the files in the directory.

    path can be specified as either str, bytes, or a path-like object.  If path is bytes,
      the filenames returned will also be bytes; in all other circumstances
      the filenames returned will be str.
    If path is None, uses the path='.'.
    On some platforms, path may also be specified as an open file descriptor;\
      the file descriptor must refer to a directory.
      If this functionality is unavailable, using it raises NotImplementedError.

    The list is in arbitrary order.  It does not include the special
    entries '.' and '..' even if they are present in the directory.
    """
    ...
@overload
def listdir(path: int) -> list[str]:
    r"""
    Return a list containing the names of the files in the directory.

    path can be specified as either str, bytes, or a path-like object.  If path is bytes,
      the filenames returned will also be bytes; in all other circumstances
      the filenames returned will be str.
    If path is None, uses the path='.'.
    On some platforms, path may also be specified as an open file descriptor;\
      the file descriptor must refer to a directory.
      If this functionality is unavailable, using it raises NotImplementedError.

    The list is in arbitrary order.  It does not include the special
    entries '.' and '..' even if they are present in the directory.
    """
    ...
@final
class DirEntry(Generic[AnyStr]):
    # This is what the scandir iterator yields
    # The constructor is hidden

    @property
    def name(self) -> AnyStr:
        """the entry's base filename, relative to scandir() "path" argument"""
        ...
    @property
    def path(self) -> AnyStr:
        """the entry's full path name; equivalent to os.path.join(scandir_path, entry.name)"""
        ...
    def inode(self) -> int:
        """Return inode of the entry; cached per entry."""
        ...
    def is_dir(self, *, follow_symlinks: bool = True) -> bool:
        """Return True if the entry is a directory; cached per entry."""
        ...
    def is_file(self, *, follow_symlinks: bool = True) -> bool:
        """Return True if the entry is a file; cached per entry."""
        ...
    def is_symlink(self) -> bool:
        """Return True if the entry is a symbolic link; cached per entry."""
        ...
    def stat(self, *, follow_symlinks: bool = True) -> stat_result:
        """Return stat_result object for the entry; cached per entry."""
        ...
    def __fspath__(self) -> AnyStr:
        """Returns the path for the entry."""
        ...
    if sys.version_info >= (3, 9):
        def __class_getitem__(cls, item: Any, /) -> GenericAlias:
            """See PEP 585"""
            ...
    if sys.version_info >= (3, 12):
        def is_junction(self) -> bool:
            """Return True if the entry is a junction; cached per entry."""
            ...

@final
class statvfs_result(structseq[int], tuple[int, int, int, int, int, int, int, int, int, int, int]):
    if sys.version_info >= (3, 10):
        __match_args__: Final = (
            "f_bsize",
            "f_frsize",
            "f_blocks",
            "f_bfree",
            "f_bavail",
            "f_files",
            "f_ffree",
            "f_favail",
            "f_flag",
            "f_namemax",
        )

    @property
    def f_bsize(self) -> int: ...
    @property
    def f_frsize(self) -> int: ...
    @property
    def f_blocks(self) -> int: ...
    @property
    def f_bfree(self) -> int: ...
    @property
    def f_bavail(self) -> int: ...
    @property
    def f_files(self) -> int: ...
    @property
    def f_ffree(self) -> int: ...
    @property
    def f_favail(self) -> int: ...
    @property
    def f_flag(self) -> int: ...
    @property
    def f_namemax(self) -> int: ...
    @property
    def f_fsid(self) -> int: ...

# ----- os function stubs -----
def fsencode(filename: StrOrBytesPath) -> bytes: ...
def fsdecode(filename: StrOrBytesPath) -> str: ...
@overload
def fspath(path: str) -> str:
    """
    Return the file system path representation of the object.

    If the object is str or bytes, then allow it to pass through as-is. If the
    object defines __fspath__(), then return the result of that method. All other
    types raise a TypeError.
    """
    ...
@overload
def fspath(path: bytes) -> bytes:
    """
    Return the file system path representation of the object.

    If the object is str or bytes, then allow it to pass through as-is. If the
    object defines __fspath__(), then return the result of that method. All other
    types raise a TypeError.
    """
    ...
@overload
def fspath(path: PathLike[AnyStr]) -> AnyStr:
    """
    Return the file system path representation of the object.

    If the object is str or bytes, then allow it to pass through as-is. If the
    object defines __fspath__(), then return the result of that method. All other
    types raise a TypeError.
    """
    ...
def get_exec_path(env: Mapping[str, str] | None = None) -> list[str]: ...
def getlogin() -> str:
    """Return the actual login name."""
    ...
def getpid() -> int:
    """Return the current process id."""
    ...
def getppid() -> int:
    """
    Return the parent's process id.

    If the parent process has already exited, Windows machines will still
    return its id; others systems will return the id of the 'init' process (1).
    """
    ...
def strerror(code: int, /) -> str:
    """Translate an error code to a message string."""
    ...
def umask(mask: int, /) -> int:
    """Set the current numeric umask and return the previous umask."""
    ...
@final
class uname_result(structseq[str], tuple[str, str, str, str, str]):
    """
    uname_result: Result from os.uname().

    This object may be accessed either as a tuple of
      (sysname, nodename, release, version, machine),
    or via the attributes sysname, nodename, release, version, and machine.

    See os.uname for more information.
    """
    if sys.version_info >= (3, 10):
        __match_args__: Final = ("sysname", "nodename", "release", "version", "machine")

    @property
    def sysname(self) -> str:
        """operating system name"""
        ...
    @property
    def nodename(self) -> str:
        """name of machine on network (implementation-defined)"""
        ...
    @property
    def release(self) -> str:
        """operating system release"""
        ...
    @property
    def version(self) -> str:
        """operating system version"""
        ...
    @property
    def machine(self) -> str:
        """hardware identifier"""
        ...

if sys.platform != "win32":
    def ctermid() -> str:
        """Return the name of the controlling terminal for this process."""
        ...
    def getegid() -> int:
        """Return the current process's effective group id."""
        ...
    def geteuid() -> int:
        """Return the current process's effective user id."""
        ...
    def getgid() -> int:
        """Return the current process's group id."""
        ...
    def getgrouplist(user: str, group: int, /) -> list[int]:
        """
        Returns a list of groups to which a user belongs.

        user
          username to lookup
        group
          base group id of the user
        """
        ...
    def getgroups() -> list[int]:
        """Return list of supplemental group IDs for the process."""
        ...
    def initgroups(username: str, gid: int, /) -> None:
        """
        Initialize the group access list.

        Call the system initgroups() to initialize the group access list with all of
        the groups of which the specified username is a member, plus the specified
        group id.
        """
        ...
    def getpgid(pid: int) -> int:
        """Call the system call getpgid(), and return the result."""
        ...
    def getpgrp() -> int:
        """Return the current process group id."""
        ...
    def getpriority(which: int, who: int) -> int:
        """Return program scheduling priority."""
        ...
    def setpriority(which: int, who: int, priority: int) -> None:
        """Set program scheduling priority."""
        ...
    if sys.platform != "darwin":
        def getresuid() -> tuple[int, int, int]:
            """Return a tuple of the current process's real, effective, and saved user ids."""
            ...
        def getresgid() -> tuple[int, int, int]:
            """Return a tuple of the current process's real, effective, and saved group ids."""
            ...

    def getuid() -> int:
        """Return the current process's user id."""
        ...
    def setegid(egid: int, /) -> None:
        """Set the current process's effective group id."""
        ...
    def seteuid(euid: int, /) -> None:
        """Set the current process's effective user id."""
        ...
    def setgid(gid: int, /) -> None:
        """Set the current process's group id."""
        ...
    def setgroups(groups: Sequence[int], /) -> None:
        """Set the groups of the current process to list."""
        ...
    def setpgrp() -> None:
        """Make the current process the leader of its process group."""
        ...
    def setpgid(pid: int, pgrp: int, /) -> None:
        """Call the system call setpgid(pid, pgrp)."""
        ...
    def setregid(rgid: int, egid: int, /) -> None:
        """Set the current process's real and effective group ids."""
        ...
    if sys.platform != "darwin":
        def setresgid(rgid: int, egid: int, sgid: int, /) -> None:
            """Set the current process's real, effective, and saved group ids."""
            ...
        def setresuid(ruid: int, euid: int, suid: int, /) -> None:
            """Set the current process's real, effective, and saved user ids."""
            ...

    def setreuid(ruid: int, euid: int, /) -> None:
        """Set the current process's real and effective user ids."""
        ...
    def getsid(pid: int, /) -> int:
        """Call the system call getsid(pid) and return the result."""
        ...
    def setsid() -> None:
        """Call the system call setsid()."""
        ...
    def setuid(uid: int, /) -> None:
        """Set the current process's user id."""
        ...
    def uname() -> uname_result:
        """
        Return an object identifying the current operating system.

        The object behaves like a named tuple with the following fields:
          (sysname, nodename, release, version, machine)
        """
        ...

@overload
def getenv(key: str) -> str | None: ...
@overload
def getenv(key: str, default: _T) -> str | _T: ...

if sys.platform != "win32":
    @overload
    def getenvb(key: bytes) -> bytes | None: ...
    @overload
    def getenvb(key: bytes, default: _T) -> bytes | _T: ...
    def putenv(name: StrOrBytesPath, value: StrOrBytesPath, /) -> None:
        """Change or add an environment variable."""
        ...
    def unsetenv(name: StrOrBytesPath, /) -> None:
        """Delete an environment variable."""
        ...

else:
    def putenv(name: str, value: str, /) -> None: ...

    if sys.version_info >= (3, 9):
        def unsetenv(name: str, /) -> None: ...

_Opener: TypeAlias = Callable[[str, int], int]

@overload
def fdopen(
    fd: int,
    mode: OpenTextMode = "r",
    buffering: int = -1,
    encoding: str | None = None,
    errors: str | None = ...,
    newline: str | None = ...,
    closefd: bool = ...,
    opener: _Opener | None = ...,
) -> TextIOWrapper: ...
@overload
def fdopen(
    fd: int,
    mode: OpenBinaryMode,
    buffering: Literal[0],
    encoding: None = None,
    errors: None = None,
    newline: None = None,
    closefd: bool = ...,
    opener: _Opener | None = ...,
) -> FileIO: ...
@overload
def fdopen(
    fd: int,
    mode: OpenBinaryModeUpdating,
    buffering: Literal[-1, 1] = -1,
    encoding: None = None,
    errors: None = None,
    newline: None = None,
    closefd: bool = ...,
    opener: _Opener | None = ...,
) -> BufferedRandom: ...
@overload
def fdopen(
    fd: int,
    mode: OpenBinaryModeWriting,
    buffering: Literal[-1, 1] = -1,
    encoding: None = None,
    errors: None = None,
    newline: None = None,
    closefd: bool = ...,
    opener: _Opener | None = ...,
) -> BufferedWriter: ...
@overload
def fdopen(
    fd: int,
    mode: OpenBinaryModeReading,
    buffering: Literal[-1, 1] = -1,
    encoding: None = None,
    errors: None = None,
    newline: None = None,
    closefd: bool = ...,
    opener: _Opener | None = ...,
) -> BufferedReader: ...
@overload
def fdopen(
    fd: int,
    mode: OpenBinaryMode,
    buffering: int = -1,
    encoding: None = None,
    errors: None = None,
    newline: None = None,
    closefd: bool = ...,
    opener: _Opener | None = ...,
) -> BinaryIO: ...
@overload
def fdopen(
    fd: int,
    mode: str,
    buffering: int = -1,
    encoding: str | None = None,
    errors: str | None = ...,
    newline: str | None = ...,
    closefd: bool = ...,
    opener: _Opener | None = ...,
) -> IO[Any]: ...
def close(fd: int) -> None:
    """Close a file descriptor."""
    ...
def closerange(fd_low: int, fd_high: int, /) -> None:
    """Closes all file descriptors in [fd_low, fd_high), ignoring errors."""
    ...
def device_encoding(fd: int) -> str | None:
    """
    Return a string describing the encoding of a terminal's file descriptor.

    The file descriptor must be attached to a terminal.
    If the device is not a terminal, return None.
    """
    ...
def dup(fd: int, /) -> int:
    """Return a duplicate of a file descriptor."""
    ...
def dup2(fd: int, fd2: int, inheritable: bool = True) -> int:
    """Duplicate file descriptor."""
    ...
def fstat(fd: int) -> stat_result:
    """
    Perform a stat system call on the given file descriptor.

    Like stat(), but for an open file descriptor.
    Equivalent to os.stat(fd).
    """
    ...
def ftruncate(fd: int, length: int, /) -> None:
    """Truncate a file, specified by file descriptor, to a specific length."""
    ...
def fsync(fd: FileDescriptorLike) -> None:
    """Force write of fd to disk."""
    ...
def isatty(fd: int, /) -> bool:
    """
    Return True if the fd is connected to a terminal.

    Return True if the file descriptor is an open file descriptor
    connected to the slave end of a terminal.
    """
    ...

if sys.platform != "win32" and sys.version_info >= (3, 11):
    def login_tty(fd: int, /) -> None:
        """
        Prepare the tty of which fd is a file descriptor for a new login session.

        Make the calling process a session leader; make the tty the
        controlling tty, the stdin, the stdout, and the stderr of the
        calling process; close fd.
        """
        ...

if sys.version_info >= (3, 11):
    def lseek(fd: int, position: int, whence: int, /) -> int:
        """
        Set the position of a file descriptor.  Return the new position.

          fd
            An open file descriptor, as returned by os.open().
          position
            Position, interpreted relative to 'whence'.
          whence
            The relative position to seek from. Valid values are:
            - SEEK_SET: seek from the start of the file.
            - SEEK_CUR: seek from the current file position.
            - SEEK_END: seek from the end of the file.

        The return value is the number of bytes relative to the beginning of the file.
        """
        ...

else:
    def lseek(fd: int, position: int, how: int, /) -> int:
        """
        Set the position of a file descriptor.  Return the new position.

        Return the new cursor position in number of bytes
        relative to the beginning of the file.
        """
        ...

def open(path: StrOrBytesPath, flags: int, mode: int = 0o777, *, dir_fd: int | None = None) -> int:
    """
    Open a file for low level IO.  Returns a file descriptor (integer).

    If dir_fd is not None, it should be a file descriptor open to a directory,
      and path should be relative; path will then be relative to that directory.
    dir_fd may not be implemented on your platform.
      If it is unavailable, using it will raise a NotImplementedError.
    """
    ...
def pipe() -> tuple[int, int]:
    """
    Create a pipe.

    Returns a tuple of two file descriptors:
      (read_fd, write_fd)
    """
    ...
def read(fd: int, length: int, /) -> bytes:
    """Read from a file descriptor.  Returns a bytes object."""
    ...

if sys.version_info >= (3, 12) or sys.platform != "win32":
    def get_blocking(fd: int, /) -> bool:
        """
        Get the blocking mode of the file descriptor.

        Return False if the O_NONBLOCK flag is set, True if the flag is cleared.
        """
        ...
    def set_blocking(fd: int, blocking: bool, /) -> None:
        """
        Set the blocking mode of the specified file descriptor.

        Set the O_NONBLOCK flag if blocking is False,
        clear the O_NONBLOCK flag otherwise.
        """
        ...

if sys.platform != "win32":
    def fchown(fd: int, uid: int, gid: int) -> None:
        """
        Change the owner and group id of the file specified by file descriptor.

        Equivalent to os.chown(fd, uid, gid).
        """
        ...
    def fpathconf(fd: int, name: str | int, /) -> int:
        """
        Return the configuration limit name for the file descriptor fd.

        If there is no limit, return -1.
        """
        ...
    def fstatvfs(fd: int, /) -> statvfs_result:
        """
        Perform an fstatvfs system call on the given fd.

        Equivalent to statvfs(fd).
        """
        ...
    def lockf(fd: int, command: int, length: int, /) -> None:
        """
        Apply, test or remove a POSIX lock on an open file descriptor.

        fd
          An open file descriptor.
        command
          One of F_LOCK, F_TLOCK, F_ULOCK or F_TEST.
        length
          The number of bytes to lock, starting at the current position.
        """
        ...
    def openpty() -> tuple[int, int]:
        """
        Open a pseudo-terminal.

        Return a tuple of (master_fd, slave_fd) containing open file descriptors
        for both the master and slave ends.
        """
        ...
    if sys.platform != "darwin":
        def fdatasync(fd: FileDescriptorLike) -> None:
            """Force write of fd to disk without forcing update of metadata."""
            ...
        def pipe2(flags: int, /) -> tuple[int, int]:
            """
            Create a pipe with flags set atomically.

            Returns a tuple of two file descriptors:
              (read_fd, write_fd)

            flags can be constructed by ORing together one or more of these values:
            O_NONBLOCK, O_CLOEXEC.
            """
            ...
        def posix_fallocate(fd: int, offset: int, length: int, /) -> None:
            """
            Ensure a file has allocated at least a particular number of bytes on disk.

            Ensure that the file specified by fd encompasses a range of bytes
            starting at offset bytes from the beginning and continuing for length bytes.
            """
            ...
        def posix_fadvise(fd: int, offset: int, length: int, advice: int, /) -> None:
            """
            Announce an intention to access data in a specific pattern.

            Announce an intention to access data in a specific pattern, thus allowing
            the kernel to make optimizations.
            The advice applies to the region of the file specified by fd starting at
            offset and continuing for length bytes.
            advice is one of POSIX_FADV_NORMAL, POSIX_FADV_SEQUENTIAL,
            POSIX_FADV_RANDOM, POSIX_FADV_NOREUSE, POSIX_FADV_WILLNEED, or
            POSIX_FADV_DONTNEED.
            """
            ...

    def pread(fd: int, length: int, offset: int, /) -> bytes:
        """
        Read a number of bytes from a file descriptor starting at a particular offset.

        Read length bytes from file descriptor fd, starting at offset bytes from
        the beginning of the file.  The file offset remains unchanged.
        """
        ...
    def pwrite(fd: int, buffer: ReadableBuffer, offset: int, /) -> int:
        """
        Write bytes to a file descriptor starting at a particular offset.

        Write buffer to fd, starting at offset bytes from the beginning of
        the file.  Returns the number of bytes written.  Does not change the
        current file offset.
        """
        ...
    # In CI, stubtest sometimes reports that these are available on MacOS, sometimes not
    def preadv(fd: int, buffers: SupportsLenAndGetItem[WriteableBuffer], offset: int, flags: int = 0, /) -> int:
        """
        Reads from a file descriptor into a number of mutable bytes-like objects.

        Combines the functionality of readv() and pread(). As readv(), it will
        transfer data into each buffer until it is full and then move on to the next
        buffer in the sequence to hold the rest of the data. Its fourth argument,
        specifies the file offset at which the input operation is to be performed. It
        will return the total number of bytes read (which can be less than the total
        capacity of all the objects).

        The flags argument contains a bitwise OR of zero or more of the following flags:

        - RWF_HIPRI
        - RWF_NOWAIT

        Using non-zero flags requires Linux 4.6 or newer.
        """
        ...
    def pwritev(fd: int, buffers: SupportsLenAndGetItem[ReadableBuffer], offset: int, flags: int = 0, /) -> int:
        """
        Writes the contents of bytes-like objects to a file descriptor at a given offset.

        Combines the functionality of writev() and pwrite(). All buffers must be a sequence
        of bytes-like objects. Buffers are processed in array order. Entire contents of first
        buffer is written before proceeding to second, and so on. The operating system may
        set a limit (sysconf() value SC_IOV_MAX) on the number of buffers that can be used.
        This function writes the contents of each object to the file descriptor and returns
        the total number of bytes written.

        The flags argument contains a bitwise OR of zero or more of the following flags:

        - RWF_DSYNC
        - RWF_SYNC
        - RWF_APPEND

        Using non-zero flags requires Linux 4.7 or newer.
        """
        ...
    if sys.platform != "darwin":
        if sys.version_info >= (3, 10):
            RWF_APPEND: int  # docs say available on 3.7+, stubtest says otherwise
        RWF_DSYNC: int
        RWF_SYNC: int
        RWF_HIPRI: int
        RWF_NOWAIT: int

    if sys.platform == "linux":
        def sendfile(out_fd: FileDescriptor, in_fd: FileDescriptor, offset: int | None, count: int) -> int: ...
    else:
        def sendfile(
            out_fd: FileDescriptor,
            in_fd: FileDescriptor,
            offset: int,
            count: int,
            headers: Sequence[ReadableBuffer] = ...,
            trailers: Sequence[ReadableBuffer] = ...,
            flags: int = 0,
        ) -> int:
            """Copy count bytes from file descriptor in_fd to file descriptor out_fd."""
            ...

    def readv(fd: int, buffers: SupportsLenAndGetItem[WriteableBuffer], /) -> int:
        """
        Read from a file descriptor fd into an iterable of buffers.

        The buffers should be mutable buffers accepting bytes.
        readv will transfer data into each buffer until it is full
        and then move on to the next buffer in the sequence to hold
        the rest of the data.

        readv returns the total number of bytes read,
        which may be less than the total capacity of all the buffers.
        """
        ...
    def writev(fd: int, buffers: SupportsLenAndGetItem[ReadableBuffer], /) -> int:
        """
        Iterate over buffers, and write the contents of each to a file descriptor.

        Returns the total number of bytes written.
        buffers must be a sequence of bytes-like objects.
        """
        ...

@final
class terminal_size(structseq[int], tuple[int, int]):
    if sys.version_info >= (3, 10):
        __match_args__: Final = ("columns", "lines")

    @property
    def columns(self) -> int:
        """width of the terminal window in characters"""
        ...
    @property
    def lines(self) -> int:
        """height of the terminal window in characters"""
        ...

def get_terminal_size(fd: int = ..., /) -> terminal_size:
    """
    Return the size of the terminal window as (columns, lines).

    The optional argument fd (default standard output) specifies
    which file descriptor should be queried.

    If the file descriptor is not connected to a terminal, an OSError
    is thrown.

    This function will only be defined if an implementation is
    available for this system.

    shutil.get_terminal_size is the high-level function which should
    normally be used, os.get_terminal_size is the low-level implementation.
    """
    ...
def get_inheritable(fd: int, /) -> bool:
    """Get the close-on-exe flag of the specified file descriptor."""
    ...
def set_inheritable(fd: int, inheritable: bool, /) -> None:
    """Set the inheritable flag of the specified file descriptor."""
    ...

if sys.platform == "win32":
    def get_handle_inheritable(handle: int, /) -> bool: ...
    def set_handle_inheritable(handle: int, inheritable: bool, /) -> None: ...

if sys.platform != "win32":
    # Unix only
    def tcgetpgrp(fd: int, /) -> int:
        """Return the process group associated with the terminal specified by fd."""
        ...
    def tcsetpgrp(fd: int, pgid: int, /) -> None:
        """Set the process group associated with the terminal specified by fd."""
        ...
    def ttyname(fd: int, /) -> str:
        """
        Return the name of the terminal device connected to 'fd'.

        fd
          Integer file descriptor handle.
        """
        ...

def write(fd: int, data: ReadableBuffer, /) -> int:
    """Write a bytes object to a file descriptor."""
    ...
def access(
    path: FileDescriptorOrPath, mode: int, *, dir_fd: int | None = None, effective_ids: bool = False, follow_symlinks: bool = True
) -> bool:
    """
    Use the real uid/gid to test for access to a path.

      path
        Path to be tested; can be string, bytes, or a path-like object.
      mode
        Operating-system mode bitfield.  Can be F_OK to test existence,
        or the inclusive-OR of R_OK, W_OK, and X_OK.
      dir_fd
        If not None, it should be a file descriptor open to a directory,
        and path should be relative; path will then be relative to that
        directory.
      effective_ids
        If True, access will use the effective uid/gid instead of
        the real uid/gid.
      follow_symlinks
        If False, and the last element of the path is a symbolic link,
        access will examine the symbolic link itself instead of the file
        the link points to.

    dir_fd, effective_ids, and follow_symlinks may not be implemented
      on your platform.  If they are unavailable, using them will raise a
      NotImplementedError.

    Note that most operations will use the effective uid/gid, therefore this
      routine can be used in a suid/sgid environment to test if the invoking user
      has the specified access to the path.
    """
    ...
def chdir(path: FileDescriptorOrPath) -> None:
    """
    Change the current working directory to the specified path.

    path may always be specified as a string.
    On some platforms, path may also be specified as an open file descriptor.
      If this functionality is unavailable, using it raises an exception.
    """
    ...

if sys.platform != "win32":
    def fchdir(fd: FileDescriptorLike) -> None:
        """
        Change to the directory of the given file descriptor.

        fd must be opened on a directory, not a file.
        Equivalent to os.chdir(fd).
        """
        ...

def getcwd() -> str:
    """Return a unicode string representing the current working directory."""
    ...
def getcwdb() -> bytes:
    """Return a bytes string representing the current working directory."""
    ...
def chmod(path: FileDescriptorOrPath, mode: int, *, dir_fd: int | None = None, follow_symlinks: bool = ...) -> None:
    """
    Change the access permissions of a file.

      path
        Path to be modified.  May always be specified as a str, bytes, or a path-like object.
        On some platforms, path may also be specified as an open file descriptor.
        If this functionality is unavailable, using it raises an exception.
      mode
        Operating-system mode bitfield.
        Be careful when using number literals for *mode*. The conventional UNIX notation for
        numeric modes uses an octal base, which needs to be indicated with a ``0o`` prefix in
        Python.
      dir_fd
        If not None, it should be a file descriptor open to a directory,
        and path should be relative; path will then be relative to that
        directory.
      follow_symlinks
        If False, and the last element of the path is a symbolic link,
        chmod will modify the symbolic link itself instead of the file
        the link points to.

    It is an error to use dir_fd or follow_symlinks when specifying path as
      an open file descriptor.
    dir_fd and follow_symlinks may not be implemented on your platform.
      If they are unavailable, using them will raise a NotImplementedError.
    """
    ...

if sys.platform != "win32" and sys.platform != "linux":
    def chflags(path: StrOrBytesPath, flags: int, follow_symlinks: bool = True) -> None:
        """
        Set file flags.

        If follow_symlinks is False, and the last element of the path is a symbolic
          link, chflags will change flags on the symbolic link itself instead of the
          file the link points to.
        follow_symlinks may not be implemented on your platform.  If it is
        unavailable, using it will raise a NotImplementedError.
        """
        ...
    def lchflags(path: StrOrBytesPath, flags: int) -> None:
        """
        Set file flags.

        This function will not follow symbolic links.
        Equivalent to chflags(path, flags, follow_symlinks=False).
        """
        ...

if sys.platform != "win32":
    def chroot(path: StrOrBytesPath) -> None:
        """Change root directory to path."""
        ...
    def chown(
        path: FileDescriptorOrPath, uid: int, gid: int, *, dir_fd: int | None = None, follow_symlinks: bool = True
    ) -> None:
        r"""
        Change the owner and group id of path to the numeric uid and gid.\

          path
            Path to be examined; can be string, bytes, a path-like object, or open-file-descriptor int.
          dir_fd
            If not None, it should be a file descriptor open to a directory,
            and path should be relative; path will then be relative to that
            directory.
          follow_symlinks
            If False, and the last element of the path is a symbolic link,
            stat will examine the symbolic link itself instead of the file
            the link points to.

        path may always be specified as a string.
        On some platforms, path may also be specified as an open file descriptor.
          If this functionality is unavailable, using it raises an exception.
        If dir_fd is not None, it should be a file descriptor open to a directory,
          and path should be relative; path will then be relative to that directory.
        If follow_symlinks is False, and the last element of the path is a symbolic
          link, chown will modify the symbolic link itself instead of the file the
          link points to.
        It is an error to use dir_fd or follow_symlinks when specifying path as
          an open file descriptor.
        dir_fd and follow_symlinks may not be implemented on your platform.
          If they are unavailable, using them will raise a NotImplementedError.
        """
        ...
    def lchown(path: StrOrBytesPath, uid: int, gid: int) -> None:
        """
        Change the owner and group id of path to the numeric uid and gid.

        This function will not follow symbolic links.
        Equivalent to os.chown(path, uid, gid, follow_symlinks=False).
        """
        ...

def link(
    src: StrOrBytesPath,
    dst: StrOrBytesPath,
    *,
    src_dir_fd: int | None = None,
    dst_dir_fd: int | None = None,
    follow_symlinks: bool = True,
) -> None:
    """
    Create a hard link to a file.

    If either src_dir_fd or dst_dir_fd is not None, it should be a file
      descriptor open to a directory, and the respective path string (src or dst)
      should be relative; the path will then be relative to that directory.
    If follow_symlinks is False, and the last element of src is a symbolic
      link, link will create a link to the symbolic link itself instead of the
      file the link points to.
    src_dir_fd, dst_dir_fd, and follow_symlinks may not be implemented on your
      platform.  If they are unavailable, using them will raise a
      NotImplementedError.
    """
    ...
def lstat(path: StrOrBytesPath, *, dir_fd: int | None = None) -> stat_result:
    """
    Perform a stat system call on the given path, without following symbolic links.

    Like stat(), but do not follow symbolic links.
    Equivalent to stat(path, follow_symlinks=False).
    """
    ...
def mkdir(path: StrOrBytesPath, mode: int = 0o777, *, dir_fd: int | None = None) -> None:
    """
    Create a directory.

    If dir_fd is not None, it should be a file descriptor open to a directory,
      and path should be relative; path will then be relative to that directory.
    dir_fd may not be implemented on your platform.
      If it is unavailable, using it will raise a NotImplementedError.

    The mode argument is ignored on Windows. Where it is used, the current umask
    value is first masked out.
    """
    ...

if sys.platform != "win32":
    def mkfifo(path: StrOrBytesPath, mode: int = 0o666, *, dir_fd: int | None = None) -> None:
        """
        Create a "fifo" (a POSIX named pipe).

        If dir_fd is not None, it should be a file descriptor open to a directory,
          and path should be relative; path will then be relative to that directory.
        dir_fd may not be implemented on your platform.
          If it is unavailable, using it will raise a NotImplementedError.
        """
        ...

def makedirs(name: StrOrBytesPath, mode: int = 0o777, exist_ok: bool = False) -> None: ...

if sys.platform != "win32":
    def mknod(path: StrOrBytesPath, mode: int = 0o600, device: int = 0, *, dir_fd: int | None = None) -> None:
        """
        Create a node in the file system.

        Create a node in the file system (file, device special file or named pipe)
        at path.  mode specifies both the permissions to use and the
        type of node to be created, being combined (bitwise OR) with one of
        S_IFREG, S_IFCHR, S_IFBLK, and S_IFIFO.  If S_IFCHR or S_IFBLK is set on mode,
        device defines the newly created device special file (probably using
        os.makedev()).  Otherwise device is ignored.

        If dir_fd is not None, it should be a file descriptor open to a directory,
          and path should be relative; path will then be relative to that directory.
        dir_fd may not be implemented on your platform.
          If it is unavailable, using it will raise a NotImplementedError.
        """
        ...
    def major(device: int, /) -> int:
        """Extracts a device major number from a raw device number."""
        ...
    def minor(device: int, /) -> int:
        """Extracts a device minor number from a raw device number."""
        ...
    def makedev(major: int, minor: int, /) -> int:
        """Composes a raw device number from the major and minor device numbers."""
        ...
    def pathconf(path: FileDescriptorOrPath, name: str | int) -> int:
        """
        Return the configuration limit name for the file or directory path.

        If there is no limit, return -1.
        On some platforms, path may also be specified as an open file descriptor.
          If this functionality is unavailable, using it raises an exception.
        """
        ...

def readlink(path: GenericPath[AnyStr], *, dir_fd: int | None = None) -> AnyStr:
    """
    Return a string representing the path to which the symbolic link points.

    If dir_fd is not None, it should be a file descriptor open to a directory,
    and path should be relative; path will then be relative to that directory.

    dir_fd may not be implemented on your platform.  If it is unavailable,
    using it will raise a NotImplementedError.
    """
    ...
def remove(path: StrOrBytesPath, *, dir_fd: int | None = None) -> None:
    """
    Remove a file (same as unlink()).

    If dir_fd is not None, it should be a file descriptor open to a directory,
      and path should be relative; path will then be relative to that directory.
    dir_fd may not be implemented on your platform.
      If it is unavailable, using it will raise a NotImplementedError.
    """
    ...
def removedirs(name: StrOrBytesPath) -> None: ...
def rename(src: StrOrBytesPath, dst: StrOrBytesPath, *, src_dir_fd: int | None = None, dst_dir_fd: int | None = None) -> None:
    """
    Rename a file or directory.

    If either src_dir_fd or dst_dir_fd is not None, it should be a file
      descriptor open to a directory, and the respective path string (src or dst)
      should be relative; the path will then be relative to that directory.
    src_dir_fd and dst_dir_fd, may not be implemented on your platform.
      If they are unavailable, using them will raise a NotImplementedError.
    """
    ...
def renames(old: StrOrBytesPath, new: StrOrBytesPath) -> None: ...
def replace(
    src: StrOrBytesPath, dst: StrOrBytesPath, *, src_dir_fd: int | None = None, dst_dir_fd: int | None = None
) -> None:
    """
    Rename a file or directory, overwriting the destination.

    If either src_dir_fd or dst_dir_fd is not None, it should be a file
      descriptor open to a directory, and the respective path string (src or dst)
      should be relative; the path will then be relative to that directory.
    src_dir_fd and dst_dir_fd, may not be implemented on your platform.
      If they are unavailable, using them will raise a NotImplementedError.
    """
    ...
def rmdir(path: StrOrBytesPath, *, dir_fd: int | None = None) -> None:
    """
    Remove a directory.

    If dir_fd is not None, it should be a file descriptor open to a directory,
      and path should be relative; path will then be relative to that directory.
    dir_fd may not be implemented on your platform.
      If it is unavailable, using it will raise a NotImplementedError.
    """
    ...

class _ScandirIterator(Iterator[DirEntry[AnyStr]], AbstractContextManager[_ScandirIterator[AnyStr], None]):
    def __next__(self) -> DirEntry[AnyStr]: ...
    def __exit__(self, *args: Unused) -> None: ...
    def close(self) -> None: ...

@overload
def scandir(path: None = None) -> _ScandirIterator[str]:
    """
    Return an iterator of DirEntry objects for given path.

    path can be specified as either str, bytes, or a path-like object.  If path
    is bytes, the names of yielded DirEntry objects will also be bytes; in
    all other circumstances they will be str.

    If path is None, uses the path='.'.
    """
    ...
@overload
def scandir(path: int) -> _ScandirIterator[str]:
    """
    Return an iterator of DirEntry objects for given path.

    path can be specified as either str, bytes, or a path-like object.  If path
    is bytes, the names of yielded DirEntry objects will also be bytes; in
    all other circumstances they will be str.

    If path is None, uses the path='.'.
    """
    ...
@overload
def scandir(path: GenericPath[AnyStr]) -> _ScandirIterator[AnyStr]:
    """
    Return an iterator of DirEntry objects for given path.

    path can be specified as either str, bytes, or a path-like object.  If path
    is bytes, the names of yielded DirEntry objects will also be bytes; in
    all other circumstances they will be str.

    If path is None, uses the path='.'.
    """
    ...
def stat(path: FileDescriptorOrPath, *, dir_fd: int | None = None, follow_symlinks: bool = True) -> stat_result:
    """
    Perform a stat system call on the given path.

      path
        Path to be examined; can be string, bytes, a path-like object or
        open-file-descriptor int.
      dir_fd
        If not None, it should be a file descriptor open to a directory,
        and path should be a relative string; path will then be relative to
        that directory.
      follow_symlinks
        If False, and the last element of the path is a symbolic link,
        stat will examine the symbolic link itself instead of the file
        the link points to.

    dir_fd and follow_symlinks may not be implemented
      on your platform.  If they are unavailable, using them will raise a
      NotImplementedError.

    It's an error to use dir_fd or follow_symlinks when specifying path as
      an open file descriptor.
    """
    ...

if sys.platform != "win32":
    def statvfs(path: FileDescriptorOrPath) -> statvfs_result:
        """
        Perform a statvfs system call on the given path.

        path may always be specified as a string.
        On some platforms, path may also be specified as an open file descriptor.
          If this functionality is unavailable, using it raises an exception.
        """
        ...

def symlink(
    src: StrOrBytesPath, dst: StrOrBytesPath, target_is_directory: bool = False, *, dir_fd: int | None = None
) -> None:
    """
    Create a symbolic link pointing to src named dst.

    target_is_directory is required on Windows if the target is to be
      interpreted as a directory.  (On Windows, symlink requires
      Windows 6.0 or greater, and raises a NotImplementedError otherwise.)
      target_is_directory is ignored on non-Windows platforms.

    If dir_fd is not None, it should be a file descriptor open to a directory,
      and path should be relative; path will then be relative to that directory.
    dir_fd may not be implemented on your platform.
      If it is unavailable, using it will raise a NotImplementedError.
    """
    ...

if sys.platform != "win32":
    def sync() -> None:
        """Force write of everything to disk."""
        ...

def truncate(path: FileDescriptorOrPath, length: int) -> None:
    """
    Truncate a file, specified by path, to a specific length.

    On some platforms, path may also be specified as an open file descriptor.
      If this functionality is unavailable, using it raises an exception.
    """
    ...
def unlink(path: StrOrBytesPath, *, dir_fd: int | None = None) -> None:
    """
    Remove a file (same as remove()).

    If dir_fd is not None, it should be a file descriptor open to a directory,
      and path should be relative; path will then be relative to that directory.
    dir_fd may not be implemented on your platform.
      If it is unavailable, using it will raise a NotImplementedError.
    """
    ...
def utime(
    path: FileDescriptorOrPath,
    times: tuple[int, int] | tuple[float, float] | None = None,
    *,
    ns: tuple[int, int] = ...,
    dir_fd: int | None = None,
    follow_symlinks: bool = True,
) -> None:
    """
    Set the access and modified time of path.

    path may always be specified as a string.
    On some platforms, path may also be specified as an open file descriptor.
      If this functionality is unavailable, using it raises an exception.

    If times is not None, it must be a tuple (atime, mtime);
        atime and mtime should be expressed as float seconds since the epoch.
    If ns is specified, it must be a tuple (atime_ns, mtime_ns);
        atime_ns and mtime_ns should be expressed as integer nanoseconds
        since the epoch.
    If times is None and ns is unspecified, utime uses the current time.
    Specifying tuples for both times and ns is an error.

    If dir_fd is not None, it should be a file descriptor open to a directory,
      and path should be relative; path will then be relative to that directory.
    If follow_symlinks is False, and the last element of the path is a symbolic
      link, utime will modify the symbolic link itself instead of the file the
      link points to.
    It is an error to use dir_fd or follow_symlinks when specifying path
      as an open file descriptor.
    dir_fd and follow_symlinks may not be available on your platform.
      If they are unavailable, using them will raise a NotImplementedError.
    """
    ...

_OnError: TypeAlias = Callable[[OSError], object]

def walk(
    top: GenericPath[AnyStr], topdown: bool = True, onerror: _OnError | None = None, followlinks: bool = False
) -> Iterator[tuple[AnyStr, list[AnyStr], list[AnyStr]]]: ...

if sys.platform != "win32":
    @overload
    def fwalk(
        top: StrPath = ".",
        topdown: bool = True,
        onerror: _OnError | None = None,
        *,
        follow_symlinks: bool = False,
        dir_fd: int | None = None,
    ) -> Iterator[tuple[str, list[str], list[str], int]]: ...
    @overload
    def fwalk(
        top: BytesPath,
        topdown: bool = True,
        onerror: _OnError | None = None,
        *,
        follow_symlinks: bool = False,
        dir_fd: int | None = None,
    ) -> Iterator[tuple[bytes, list[bytes], list[bytes], int]]: ...
    if sys.platform == "linux":
        def getxattr(path: FileDescriptorOrPath, attribute: StrOrBytesPath, *, follow_symlinks: bool = True) -> bytes: ...
        def listxattr(path: FileDescriptorOrPath | None = None, *, follow_symlinks: bool = True) -> list[str]: ...
        def removexattr(path: FileDescriptorOrPath, attribute: StrOrBytesPath, *, follow_symlinks: bool = True) -> None: ...
        def setxattr(
            path: FileDescriptorOrPath,
            attribute: StrOrBytesPath,
            value: ReadableBuffer,
            flags: int = 0,
            *,
            follow_symlinks: bool = True,
        ) -> None: ...

def abort() -> NoReturn:
    """
    Abort the interpreter immediately.

    This function 'dumps core' or otherwise fails in the hardest way possible
    on the hosting operating system.  This function never returns.
    """
    ...

# These are defined as execl(file, *args) but the first *arg is mandatory.
def execl(file: StrOrBytesPath, *args: Unpack[tuple[StrOrBytesPath, Unpack[tuple[StrOrBytesPath, ...]]]]) -> NoReturn: ...
def execlp(file: StrOrBytesPath, *args: Unpack[tuple[StrOrBytesPath, Unpack[tuple[StrOrBytesPath, ...]]]]) -> NoReturn: ...

# These are: execle(file, *args, env) but env is pulled from the last element of the args.
def execle(
    file: StrOrBytesPath, *args: Unpack[tuple[StrOrBytesPath, Unpack[tuple[StrOrBytesPath, ...]], _ExecEnv]]
) -> NoReturn: ...
def execlpe(
    file: StrOrBytesPath, *args: Unpack[tuple[StrOrBytesPath, Unpack[tuple[StrOrBytesPath, ...]], _ExecEnv]]
) -> NoReturn: ...

# The docs say `args: tuple or list of strings`
# The implementation enforces tuple or list so we can't use Sequence.
# Not separating out PathLike[str] and PathLike[bytes] here because it doesn't make much difference
# in practice, and doing so would explode the number of combinations in this already long union.
# All these combinations are necessary due to list being invariant.
_ExecVArgs: TypeAlias = (
    tuple[StrOrBytesPath, ...]
    | list[bytes]
    | list[str]
    | list[PathLike[Any]]
    | list[bytes | str]
    | list[bytes | PathLike[Any]]
    | list[str | PathLike[Any]]
    | list[bytes | str | PathLike[Any]]
)
# Depending on the OS, the keys and values are passed either to
# PyUnicode_FSDecoder (which accepts str | ReadableBuffer) or to
# PyUnicode_FSConverter (which accepts StrOrBytesPath). For simplicity,
# we limit to str | bytes.
_ExecEnv: TypeAlias = Mapping[bytes, bytes | str] | Mapping[str, bytes | str]

def execv(path: StrOrBytesPath, argv: _ExecVArgs, /) -> NoReturn:
    """
    Execute an executable path with arguments, replacing current process.

    path
      Path of executable file.
    argv
      Tuple or list of strings.
    """
    ...
def execve(path: FileDescriptorOrPath, argv: _ExecVArgs, env: _ExecEnv) -> NoReturn:
    """
    Execute an executable path with arguments, replacing current process.

    path
      Path of executable file.
    argv
      Tuple or list of strings.
    env
      Dictionary of strings mapping to strings.
    """
    ...
def execvp(file: StrOrBytesPath, args: _ExecVArgs) -> NoReturn: ...
def execvpe(file: StrOrBytesPath, args: _ExecVArgs, env: _ExecEnv) -> NoReturn: ...
def _exit(status: int) -> NoReturn:
    """Exit to the system with specified status, without normal exit processing."""
    ...
def kill(pid: int, signal: int, /) -> None:
    """Kill a process with a signal."""
    ...

if sys.platform != "win32":
    # Unix only
    def fork() -> int:
        """
        Fork a child process.

        Return 0 to child process and PID of child to parent process.
        """
        ...
    def forkpty() -> tuple[int, int]:
        """
        Fork a new process with a new pseudo-terminal as controlling tty.

        Returns a tuple of (pid, master_fd).
        Like fork(), return pid of 0 to the child process,
        and pid of child to the parent process.
        To both, return fd of newly opened pseudo-terminal.
        """
        ...
    def killpg(pgid: int, signal: int, /) -> None:
        """Kill a process group with a signal."""
        ...
    def nice(increment: int, /) -> int:
        """Add increment to the priority of process and return the new priority."""
        ...
    if sys.platform != "darwin" and sys.platform != "linux":
        def plock(op: int, /) -> None: ...

class _wrap_close:
    def __init__(self, stream: TextIOWrapper, proc: Popen[str]) -> None: ...
    def close(self) -> int | None: ...
    def __enter__(self) -> Self: ...
    def __exit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None
    ) -> None: ...
    def __iter__(self) -> Iterator[str]: ...
    # Methods below here don't exist directly on the _wrap_close object, but
    # are copied from the wrapped TextIOWrapper object via __getattr__.
    # The full set of TextIOWrapper methods are technically available this way,
    # but undocumented. Only a subset are currently included here.
    def read(self, size: int | None = -1, /) -> str: ...
    def readable(self) -> bool: ...
    def readline(self, size: int = -1, /) -> str: ...
    def readlines(self, hint: int = -1, /) -> list[str]: ...
    def writable(self) -> bool: ...
    def write(self, s: str, /) -> int: ...
    def writelines(self, lines: Iterable[str], /) -> None: ...

def popen(cmd: str, mode: str = "r", buffering: int = -1) -> _wrap_close: ...
def spawnl(mode: int, file: StrOrBytesPath, arg0: StrOrBytesPath, *args: StrOrBytesPath) -> int: ...
def spawnle(mode: int, file: StrOrBytesPath, arg0: StrOrBytesPath, *args: Any) -> int: ...  # Imprecise sig

if sys.platform != "win32":
    def spawnv(mode: int, file: StrOrBytesPath, args: _ExecVArgs) -> int:
        """
        Execute the program specified by path in a new process.

        mode
          Mode of process creation.
        path
          Path of executable file.
        argv
          Tuple or list of strings.
        """
        ...
    def spawnve(mode: int, file: StrOrBytesPath, args: _ExecVArgs, env: _ExecEnv) -> int:
        """
        Execute the program specified by path in a new process.

        mode
          Mode of process creation.
        path
          Path of executable file.
        argv
          Tuple or list of strings.
        env
          Dictionary of strings mapping to strings.
        """
        ...

else:
    def spawnv(mode: int, path: StrOrBytesPath, argv: _ExecVArgs, /) -> int: ...
    def spawnve(mode: int, path: StrOrBytesPath, argv: _ExecVArgs, env: _ExecEnv, /) -> int: ...

def system(command: StrOrBytesPath) -> int:
    """Execute the command in a subshell."""
    ...
@final
class times_result(structseq[float], tuple[float, float, float, float, float]):
    """
    times_result: Result from os.times().

    This object may be accessed either as a tuple of
      (user, system, children_user, children_system, elapsed),
    or via the attributes user, system, children_user, children_system,
    and elapsed.

    See os.times for more information.
    """
    if sys.version_info >= (3, 10):
        __match_args__: Final = ("user", "system", "children_user", "children_system", "elapsed")

    @property
    def user(self) -> float:
        """user time"""
        ...
    @property
    def system(self) -> float:
        """system time"""
        ...
    @property
    def children_user(self) -> float:
        """user time of children"""
        ...
    @property
    def children_system(self) -> float:
        """system time of children"""
        ...
    @property
    def elapsed(self) -> float:
        """elapsed time since an arbitrary point in the past"""
        ...

def times() -> times_result:
    """
    Return a collection containing process timing information.

    The object returned behaves like a named tuple with these fields:
      (utime, stime, cutime, cstime, elapsed_time)
    All fields are floating-point numbers.
    """
    ...
def waitpid(pid: int, options: int, /) -> tuple[int, int]:
    """
    Wait for completion of a given child process.

    Returns a tuple of information regarding the child process:
        (pid, status)

    The options argument is ignored on Windows.
    """
    ...

if sys.platform == "win32":
    if sys.version_info >= (3, 10):
        def startfile(
            filepath: StrOrBytesPath,
            operation: str = ...,
            arguments: str = "",
            cwd: StrOrBytesPath | None = None,
            show_cmd: int = 1,
        ) -> None: ...
    else:
        def startfile(filepath: StrOrBytesPath, operation: str = ...) -> None: ...

else:
    def spawnlp(mode: int, file: StrOrBytesPath, arg0: StrOrBytesPath, *args: StrOrBytesPath) -> int: ...
    def spawnlpe(mode: int, file: StrOrBytesPath, arg0: StrOrBytesPath, *args: Any) -> int: ...  # Imprecise signature
    def spawnvp(mode: int, file: StrOrBytesPath, args: _ExecVArgs) -> int: ...
    def spawnvpe(mode: int, file: StrOrBytesPath, args: _ExecVArgs, env: _ExecEnv) -> int: ...
    def wait() -> tuple[int, int]:
        """
        Wait for completion of a child process.

        Returns a tuple of information about the child process:
            (pid, status)
        """
        ...
    # Added to MacOS in 3.13
    if sys.platform != "darwin" or sys.version_info >= (3, 13):
        @final
        class waitid_result(structseq[int], tuple[int, int, int, int, int]):
            """
            waitid_result: Result from waitid.

            This object may be accessed either as a tuple of
              (si_pid, si_uid, si_signo, si_status, si_code),
            or via the attributes si_pid, si_uid, and so on.

            See os.waitid for more information.
            """
            if sys.version_info >= (3, 10):
                __match_args__: Final = ("si_pid", "si_uid", "si_signo", "si_status", "si_code")

            @property
            def si_pid(self) -> int: ...
            @property
            def si_uid(self) -> int: ...
            @property
            def si_signo(self) -> int: ...
            @property
            def si_status(self) -> int: ...
            @property
            def si_code(self) -> int: ...

        def waitid(idtype: int, ident: int, options: int, /) -> waitid_result | None:
            """
            Returns the result of waiting for a process or processes.

              idtype
                Must be one of be P_PID, P_PGID or P_ALL.
              id
                The id to wait on.
              options
                Constructed from the ORing of one or more of WEXITED, WSTOPPED
                or WCONTINUED and additionally may be ORed with WNOHANG or WNOWAIT.

            Returns either waitid_result or None if WNOHANG is specified and there are
            no children in a waitable state.
            """
            ...

    from resource import struct_rusage

    def wait3(options: int) -> tuple[int, int, struct_rusage]:
        """
        Wait for completion of a child process.

        Returns a tuple of information about the child process:
          (pid, status, rusage)
        """
        ...
    def wait4(pid: int, options: int) -> tuple[int, int, struct_rusage]:
        """
        Wait for completion of a specific child process.

        Returns a tuple of information about the child process:
          (pid, status, rusage)
        """
        ...
    def WCOREDUMP(status: int, /) -> bool:
        """Return True if the process returning status was dumped to a core file."""
        ...
    def WIFCONTINUED(status: int) -> bool:
        """
        Return True if a particular process was continued from a job control stop.

        Return True if the process returning status was continued from a
        job control stop.
        """
        ...
    def WIFSTOPPED(status: int) -> bool:
        """Return True if the process returning status was stopped."""
        ...
    def WIFSIGNALED(status: int) -> bool:
        """Return True if the process returning status was terminated by a signal."""
        ...
    def WIFEXITED(status: int) -> bool:
        """Return True if the process returning status exited via the exit() system call."""
        ...
    def WEXITSTATUS(status: int) -> int:
        """Return the process return code from status."""
        ...
    def WSTOPSIG(status: int) -> int:
        """Return the signal that stopped the process that provided the status value."""
        ...
    def WTERMSIG(status: int) -> int:
        """Return the signal that terminated the process that provided the status value."""
        ...
    def posix_spawn(
        path: StrOrBytesPath,
        argv: _ExecVArgs,
        env: _ExecEnv,
        /,
        *,
        file_actions: Sequence[tuple[Any, ...]] | None = ...,
        setpgroup: int | None = ...,
        resetids: bool = ...,
        setsid: bool = ...,
        setsigmask: Iterable[int] = ...,
        setsigdef: Iterable[int] = ...,
        scheduler: tuple[Any, sched_param] | None = ...,
    ) -> int:
        """
        Execute the program specified by path in a new process.

        path
          Path of executable file.
        argv
          Tuple or list of strings.
        env
          Dictionary of strings mapping to strings.
        file_actions
          A sequence of file action tuples.
        setpgroup
          The pgroup to use with the POSIX_SPAWN_SETPGROUP flag.
        resetids
          If the value is `true` the POSIX_SPAWN_RESETIDS will be activated.
        setsid
          If the value is `true` the POSIX_SPAWN_SETSID or POSIX_SPAWN_SETSID_NP will be activated.
        setsigmask
          The sigmask to use with the POSIX_SPAWN_SETSIGMASK flag.
        setsigdef
          The sigmask to use with the POSIX_SPAWN_SETSIGDEF flag.
        scheduler
          A tuple with the scheduler policy (optional) and parameters.
        """
        ...
    def posix_spawnp(
        path: StrOrBytesPath,
        argv: _ExecVArgs,
        env: _ExecEnv,
        /,
        *,
        file_actions: Sequence[tuple[Any, ...]] | None = ...,
        setpgroup: int | None = ...,
        resetids: bool = ...,
        setsid: bool = ...,
        setsigmask: Iterable[int] = ...,
        setsigdef: Iterable[int] = ...,
        scheduler: tuple[Any, sched_param] | None = ...,
    ) -> int:
        """
        Execute the program specified by path in a new process.

        path
          Path of executable file.
        argv
          Tuple or list of strings.
        env
          Dictionary of strings mapping to strings.
        file_actions
          A sequence of file action tuples.
        setpgroup
          The pgroup to use with the POSIX_SPAWN_SETPGROUP flag.
        resetids
          If the value is `True` the POSIX_SPAWN_RESETIDS will be activated.
        setsid
          If the value is `True` the POSIX_SPAWN_SETSID or POSIX_SPAWN_SETSID_NP will be activated.
        setsigmask
          The sigmask to use with the POSIX_SPAWN_SETSIGMASK flag.
        setsigdef
          The sigmask to use with the POSIX_SPAWN_SETSIGDEF flag.
        scheduler
          A tuple with the scheduler policy (optional) and parameters.
        """
        ...
    POSIX_SPAWN_OPEN: int
    POSIX_SPAWN_CLOSE: int
    POSIX_SPAWN_DUP2: int

if sys.platform != "win32":
    @final
    class sched_param(structseq[int], tuple[int]):
        """
        Currently has only one field: sched_priority

        sched_priority
          A scheduling parameter.
        """
        if sys.version_info >= (3, 10):
            __match_args__: Final = ("sched_priority",)

        def __new__(cls, sched_priority: int) -> Self: ...
        @property
        def sched_priority(self) -> int:
            """the scheduling priority"""
            ...

    def sched_get_priority_min(policy: int) -> int:
        """Get the minimum scheduling priority for policy."""
        ...
    def sched_get_priority_max(policy: int) -> int:
        """Get the maximum scheduling priority for policy."""
        ...
    def sched_yield() -> None:
        """Voluntarily relinquish the CPU."""
        ...
    if sys.platform != "darwin":
        def sched_setscheduler(pid: int, policy: int, param: sched_param, /) -> None:
            """
            Set the scheduling policy for the process identified by pid.

            If pid is 0, the calling process is changed.
            param is an instance of sched_param.
            """
            ...
        def sched_getscheduler(pid: int, /) -> int:
            """
            Get the scheduling policy for the process identified by pid.

            Passing 0 for pid returns the scheduling policy for the calling process.
            """
            ...
        def sched_rr_get_interval(pid: int, /) -> float:
            """
            Return the round-robin quantum for the process identified by pid, in seconds.

            Value returned is a float.
            """
            ...
        def sched_setparam(pid: int, param: sched_param, /) -> None:
            """
            Set scheduling parameters for the process identified by pid.

            If pid is 0, sets parameters for the calling process.
            param should be an instance of sched_param.
            """
            ...
        def sched_getparam(pid: int, /) -> sched_param:
            """
            Returns scheduling parameters for the process identified by pid.

            If pid is 0, returns parameters for the calling process.
            Return value is an instance of sched_param.
            """
            ...
        def sched_setaffinity(pid: int, mask: Iterable[int], /) -> None:
            """
            Set the CPU affinity of the process identified by pid to mask.

            mask should be an iterable of integers identifying CPUs.
            """
            ...
        def sched_getaffinity(pid: int, /) -> set[int]:
            """
            Return the affinity of the process identified by pid (or the current process if zero).

            The affinity is returned as a set of CPU identifiers.
            """
            ...

def cpu_count() -> int | None:
    """
    Return the number of logical CPUs in the system.

    Return None if indeterminable.
    """
    ...

if sys.platform != "win32":
    # Unix only
    def confstr(name: str | int, /) -> str | None:
        """Return a string-valued system configuration variable."""
        ...
    def getloadavg() -> tuple[float, float, float]:
        """
        Return average recent system load information.

        Return the number of processes in the system run queue averaged over
        the last 1, 5, and 15 minutes as a tuple of three floats.
        Raises OSError if the load average was unobtainable.
        """
        ...
    def sysconf(name: str | int, /) -> int:
        """Return an integer-valued system configuration variable."""
        ...

if sys.platform == "linux":
    def getrandom(size: int, flags: int = 0) -> bytes: ...

def urandom(size: int, /) -> bytes:
    """Return a bytes object containing random bytes suitable for cryptographic use."""
    ...

if sys.platform != "win32":
    def register_at_fork(
        *,
        before: Callable[..., Any] | None = ...,
        after_in_parent: Callable[..., Any] | None = ...,
        after_in_child: Callable[..., Any] | None = ...,
    ) -> None:
        """
        Register callables to be called when forking a new process.

          before
            A callable to be called in the parent before the fork() syscall.
          after_in_child
            A callable to be called in the child after fork().
          after_in_parent
            A callable to be called in the parent after fork().

        'before' callbacks are called in reverse order.
        'after_in_child' and 'after_in_parent' callbacks are called in order.
        """
        ...

if sys.platform == "win32":
    class _AddedDllDirectory:
        path: str | None
        def __init__(self, path: str | None, cookie: _T, remove_dll_directory: Callable[[_T], object]) -> None: ...
        def close(self) -> None: ...
        def __enter__(self) -> Self: ...
        def __exit__(self, *args: Unused) -> None: ...

    def add_dll_directory(path: str) -> _AddedDllDirectory: ...

if sys.platform == "linux":
    MFD_CLOEXEC: int
    MFD_ALLOW_SEALING: int
    MFD_HUGETLB: int
    MFD_HUGE_SHIFT: int
    MFD_HUGE_MASK: int
    MFD_HUGE_64KB: int
    MFD_HUGE_512KB: int
    MFD_HUGE_1MB: int
    MFD_HUGE_2MB: int
    MFD_HUGE_8MB: int
    MFD_HUGE_16MB: int
    MFD_HUGE_32MB: int
    MFD_HUGE_256MB: int
    MFD_HUGE_512MB: int
    MFD_HUGE_1GB: int
    MFD_HUGE_2GB: int
    MFD_HUGE_16GB: int
    def memfd_create(name: str, flags: int = ...) -> int: ...
    def copy_file_range(src: int, dst: int, count: int, offset_src: int | None = ..., offset_dst: int | None = ...) -> int: ...

if sys.version_info >= (3, 9):
    def waitstatus_to_exitcode(status: int) -> int:
        """
        Convert a wait status to an exit code.

        On Unix:

        * If WIFEXITED(status) is true, return WEXITSTATUS(status).
        * If WIFSIGNALED(status) is true, return -WTERMSIG(status).
        * Otherwise, raise a ValueError.

        On Windows, return status shifted right by 8 bits.

        On Unix, if the process is being traced or if waitpid() was called with
        WUNTRACED option, the caller must first check if WIFSTOPPED(status) is true.
        This function must not be called if WIFSTOPPED(status) is true.
        """
        ...

    if sys.platform == "linux":
        def pidfd_open(pid: int, flags: int = ...) -> int: ...

if sys.version_info >= (3, 12) and sys.platform == "win32":
    def listdrives() -> list[str]: ...
    def listmounts(volume: str) -> list[str]: ...
    def listvolumes() -> list[str]: ...

if sys.version_info >= (3, 10) and sys.platform == "linux":
    EFD_CLOEXEC: int
    EFD_NONBLOCK: int
    EFD_SEMAPHORE: int
    SPLICE_F_MORE: int
    SPLICE_F_MOVE: int
    SPLICE_F_NONBLOCK: int
    def eventfd(initval: int, flags: int = 524288) -> FileDescriptor: ...
    def eventfd_read(fd: FileDescriptor) -> int: ...
    def eventfd_write(fd: FileDescriptor, value: int) -> None: ...
    def splice(
        src: FileDescriptor,
        dst: FileDescriptor,
        count: int,
        offset_src: int | None = ...,
        offset_dst: int | None = ...,
        flags: int = 0,
    ) -> int: ...

if sys.version_info >= (3, 12) and sys.platform == "linux":
    CLONE_FILES: int
    CLONE_FS: int
    CLONE_NEWCGROUP: int  # Linux 4.6+
    CLONE_NEWIPC: int  # Linux 2.6.19+
    CLONE_NEWNET: int  # Linux 2.6.24+
    CLONE_NEWNS: int
    CLONE_NEWPID: int  # Linux 3.8+
    CLONE_NEWTIME: int  # Linux 5.6+
    CLONE_NEWUSER: int  # Linux 3.8+
    CLONE_NEWUTS: int  # Linux 2.6.19+
    CLONE_SIGHAND: int
    CLONE_SYSVSEM: int  # Linux 2.6.26+
    CLONE_THREAD: int
    CLONE_VM: int
    def unshare(flags: int) -> None: ...
    def setns(fd: FileDescriptorLike, nstype: int = 0) -> None: ...

if sys.version_info >= (3, 13) and sys.platform != "win32":
    def posix_openpt(oflag: int, /) -> int:
        """
        Open and return a file descriptor for a master pseudo-terminal device.

        Performs a posix_openpt() C function call. The oflag argument is used to
        set file status flags and file access modes as specified in the manual page
        of posix_openpt() of your system.
        """
        ...
    def grantpt(fd: FileDescriptorLike, /) -> None:
        """
        Grant access to the slave pseudo-terminal device.

          fd
            File descriptor of a master pseudo-terminal device.

        Performs a grantpt() C function call.
        """
        ...
    def unlockpt(fd: FileDescriptorLike, /) -> None:
        """
        Unlock a pseudo-terminal master/slave pair.

          fd
            File descriptor of a master pseudo-terminal device.

        Performs an unlockpt() C function call.
        """
        ...
    def ptsname(fd: FileDescriptorLike, /) -> str:
        """
        Return the name of the slave pseudo-terminal device.

          fd
            File descriptor of a master pseudo-terminal device.

        If the ptsname_r() C function is available, it is called;
        otherwise, performs a ptsname() C function call.
        """
        ...

if sys.version_info >= (3, 13) and sys.platform == "linux":
    TFD_TIMER_ABSTIME: Final = 1
    TFD_TIMER_CANCEL_ON_SET: Final = 2
    TFD_NONBLOCK: Final[int]
    TFD_CLOEXEC: Final[int]
    POSIX_SPAWN_CLOSEFROM: Final[int]

    def timerfd_create(clockid: int, /, *, flags: int = 0) -> int: ...
    def timerfd_settime(
        fd: FileDescriptor, /, *, flags: int = 0, initial: float = 0.0, interval: float = 0.0
    ) -> tuple[float, float]: ...
    def timerfd_settime_ns(fd: FileDescriptor, /, *, flags: int = 0, initial: int = 0, interval: int = 0) -> tuple[int, int]: ...
    def timerfd_gettime(fd: FileDescriptor, /) -> tuple[float, float]: ...
    def timerfd_gettime_ns(fd: FileDescriptor, /) -> tuple[int, int]: ...

if sys.version_info >= (3, 13) or sys.platform != "win32":
    # Added to Windows in 3.13.
    def fchmod(fd: int, mode: int) -> None:
        """
        Change the access permissions of the file given by file descriptor fd.

          fd
            The file descriptor of the file to be modified.
          mode
            Operating-system mode bitfield.
            Be careful when using number literals for *mode*. The conventional UNIX notation for
            numeric modes uses an octal base, which needs to be indicated with a ``0o`` prefix in
            Python.

        Equivalent to os.chmod(fd, mode).
        """
        ...

if sys.platform != "linux":
    if sys.version_info >= (3, 13) or sys.platform != "win32":
        # Added to Windows in 3.13.
        def lchmod(path: StrOrBytesPath, mode: int) -> None:
            """
            Change the access permissions of a file, without following symbolic links.

            If path is a symlink, this affects the link itself rather than the target.
            Equivalent to chmod(path, mode, follow_symlinks=False)."
            """
            ...
