import pygit2.enums

class SearchPathList:
    def __getitem__(self, key: int) -> str: ...
    def __setitem__(self, key: int, value: bytes | str) -> None: ...

class Settings:
    def __init__(self) -> None: ...
    @property
    def search_path(self) -> SearchPathList: ...
    @property
    def mwindow_size(self) -> int: ...
    @mwindow_size.setter
    def mwindow_size(self, value: int) -> None: ...
    @property
    def mwindow_mapped_limit(self) -> int: ...
    @mwindow_mapped_limit.setter
    def mwindow_mapped_limit(self, value: int) -> None: ...
    @property
    def cached_memory(self) -> tuple[int, int]: ...
    def enable_caching(self, value: bool = True) -> None: ...
    def disable_pack_keep_file_checks(self, value: bool = True) -> None: ...
    def cache_max_size(self, value: int) -> None: ...
    def cache_object_limit(self, object_type: pygit2.enums.ObjectType, value: int) -> None: ...
    @property
    def ssl_cert_file(self) -> bytes | str: ...
    @ssl_cert_file.setter
    def ssl_cert_file(self, value: bytes | str) -> None: ...
    @ssl_cert_file.deleter
    def ssl_cert_file(self) -> None: ...
    @property
    def ssl_cert_dir(self) -> bytes | str: ...
    @ssl_cert_dir.setter
    def ssl_cert_dir(self, value: bytes | str) -> None: ...
    @ssl_cert_dir.deleter
    def ssl_cert_dir(self) -> None: ...
    def set_ssl_cert_locations(self, cert_file: bytes | str, cert_dir: bytes | str) -> None: ...
