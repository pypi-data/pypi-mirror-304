"""
This module provides access to operating system functionality that is
standardized by the C Standard and the POSIX standard (a thinly
disguised Unix interface).  Refer to the library manual and
corresponding Unix manual entries for more information on calls.
"""

import sys

if sys.platform == "win32":
    # Actually defined here and re-exported from os at runtime,
    # but this leads to less code duplication
    from os import (
        F_OK as F_OK,
        O_APPEND as O_APPEND,
        O_BINARY as O_BINARY,
        O_CREAT as O_CREAT,
        O_EXCL as O_EXCL,
        O_NOINHERIT as O_NOINHERIT,
        O_RANDOM as O_RANDOM,
        O_RDONLY as O_RDONLY,
        O_RDWR as O_RDWR,
        O_SEQUENTIAL as O_SEQUENTIAL,
        O_SHORT_LIVED as O_SHORT_LIVED,
        O_TEMPORARY as O_TEMPORARY,
        O_TEXT as O_TEXT,
        O_TRUNC as O_TRUNC,
        O_WRONLY as O_WRONLY,
        P_DETACH as P_DETACH,
        P_NOWAIT as P_NOWAIT,
        P_NOWAITO as P_NOWAITO,
        P_OVERLAY as P_OVERLAY,
        P_WAIT as P_WAIT,
        R_OK as R_OK,
        TMP_MAX as TMP_MAX,
        W_OK as W_OK,
        X_OK as X_OK,
        DirEntry as DirEntry,
        abort as abort,
        access as access,
        chdir as chdir,
        chmod as chmod,
        close as close,
        closerange as closerange,
        cpu_count as cpu_count,
        device_encoding as device_encoding,
        dup as dup,
        dup2 as dup2,
        error as error,
        execv as execv,
        execve as execve,
        fspath as fspath,
        fstat as fstat,
        fsync as fsync,
        ftruncate as ftruncate,
        get_handle_inheritable as get_handle_inheritable,
        get_inheritable as get_inheritable,
        get_terminal_size as get_terminal_size,
        getcwd as getcwd,
        getcwdb as getcwdb,
        getlogin as getlogin,
        getpid as getpid,
        getppid as getppid,
        isatty as isatty,
        kill as kill,
        link as link,
        listdir as listdir,
        lseek as lseek,
        lstat as lstat,
        mkdir as mkdir,
        open as open,
        pipe as pipe,
        putenv as putenv,
        read as read,
        readlink as readlink,
        remove as remove,
        rename as rename,
        replace as replace,
        rmdir as rmdir,
        scandir as scandir,
        set_handle_inheritable as set_handle_inheritable,
        set_inheritable as set_inheritable,
        spawnv as spawnv,
        spawnve as spawnve,
        startfile as startfile,
        stat as stat,
        stat_result as stat_result,
        statvfs_result as statvfs_result,
        strerror as strerror,
        symlink as symlink,
        system as system,
        terminal_size as terminal_size,
        times as times,
        times_result as times_result,
        truncate as truncate,
        umask as umask,
        uname_result as uname_result,
        unlink as unlink,
        urandom as urandom,
        utime as utime,
        waitpid as waitpid,
        write as write,
    )

    if sys.version_info >= (3, 9):
        from os import unsetenv as unsetenv, waitstatus_to_exitcode as waitstatus_to_exitcode
    if sys.version_info >= (3, 11):
        from os import EX_OK as EX_OK
    if sys.version_info >= (3, 12):
        from os import (
            get_blocking as get_blocking,
            listdrives as listdrives,
            listmounts as listmounts,
            listvolumes as listvolumes,
            set_blocking as set_blocking,
        )
    if sys.version_info >= (3, 13):
        from os import fchmod as fchmod, lchmod as lchmod

    environ: dict[str, str]
