import datetime
from _typeshed import Incomplete, Unused
from collections.abc import Iterator
from enum import Enum
from re import Pattern
from typing import Any, ClassVar, Final, TypeVar, overload
from typing_extensions import Self, TypeAlias

from .caselessdict import CaselessDict
from .parser import Parameters
from .parser_tools import ICAL_TYPE

__all__ = [
    "DURATION_REGEX",
    "TimeBase",
    "TypesFactory",
    "WEEKDAY_RULE",
    "tzid_from_dt",
    "vBinary",
    "vBoolean",
    "vCalAddress",
    "vCategory",
    "vDDDLists",
    "vDDDTypes",
    "vDate",
    "vDatetime",
    "vDuration",
    "vFloat",
    "vFrequency",
    "vGeo",
    "vInline",
    "vInt",
    "vMonth",
    "vPeriod",
    "vRecur",
    "vSkip",
    "vText",
    "vTime",
    "vUTCOffset",
    "vUri",
    "vWeekday",
]

_PropType: TypeAlias = type[Any]  # any of the v* classes in this file
_vRecurT = TypeVar("_vRecurT", bound=vRecur)

DURATION_REGEX: Final[Pattern[str]]
WEEKDAY_RULE: Final[Pattern[str]]

def tzid_from_dt(dt: datetime.datetime) -> str | None: ...

class vBinary:
    obj: Incomplete
    params: Parameters
    def __init__(self, obj) -> None: ...
    def to_ical(self) -> bytes: ...
    @staticmethod
    def from_ical(ical): ...
    def __eq__(self, other): ...

class vBoolean(int):
    BOOL_MAP: Incomplete
    params: Parameters
    def __new__(cls, *args, **kwargs): ...
    def to_ical(self) -> bytes: ...
    @classmethod
    def from_ical(cls, ical): ...

class vText(str):
    encoding: str
    params: Parameters
    def __new__(cls, value: ICAL_TYPE, encoding: str = "utf-8") -> Self: ...
    def to_ical(self) -> bytes: ...
    @classmethod
    def from_ical(cls, ical: ICAL_TYPE) -> Self: ...

class vCalAddress(str):
    params: Parameters
    def __new__(cls, value, encoding="utf-8"): ...
    def to_ical(self) -> bytes: ...
    @classmethod
    def from_ical(cls, ical): ...

class vFloat(float):
    params: Parameters
    def __new__(cls, *args, **kwargs): ...
    def to_ical(self) -> bytes: ...
    @classmethod
    def from_ical(cls, ical): ...

class vInt(int):
    params: Parameters
    def __new__(cls, *args, **kwargs): ...
    def to_ical(self) -> bytes: ...
    @classmethod
    def from_ical(cls, ical: ICAL_TYPE) -> Self: ...

class vDDDLists:
    params: Parameters
    dts: Incomplete
    def __init__(self, dt_list) -> None: ...
    def to_ical(self) -> bytes: ...
    @staticmethod
    def from_ical(ical, timezone: Incomplete | None = None): ...
    def __eq__(self, other): ...

class vCategory:
    cats: Incomplete
    params: Parameters
    def __init__(self, c_list) -> None: ...
    def __iter__(self) -> Iterator[str]: ...
    def to_ical(self) -> bytes: ...
    @staticmethod
    def from_ical(ical: ICAL_TYPE) -> str: ...
    def __eq__(self, other: object) -> bool: ...

class TimeBase:
    def __eq__(self, other: object) -> bool: ...
    def __hash__(self): ...

class vDDDTypes(TimeBase):
    params: Parameters
    dt: Incomplete
    def __init__(self, dt) -> None: ...
    def to_ical(self) -> bytes: ...
    @classmethod
    def from_ical(cls, ical, timezone: Incomplete | None = None): ...

class vDate(TimeBase):
    dt: Incomplete
    params: Parameters
    def __init__(self, dt) -> None: ...
    def to_ical(self) -> bytes: ...
    @staticmethod
    def from_ical(ical): ...

class vDatetime(TimeBase):
    dt: Incomplete
    params: Parameters
    def __init__(self, dt) -> None: ...
    def to_ical(self) -> bytes: ...
    @staticmethod
    def from_ical(ical, timezone: str | None = None) -> datetime.datetime: ...

class vDuration(TimeBase):
    td: Incomplete
    params: Parameters
    def __init__(self, td) -> None: ...
    def to_ical(self) -> bytes: ...
    @staticmethod
    def from_ical(ical): ...
    @property
    def dt(self): ...

class vPeriod(TimeBase):
    params: Parameters
    start: Incomplete
    end: Incomplete
    by_duration: Incomplete
    duration: Incomplete
    def __init__(self, per) -> None: ...
    def overlaps(self, other): ...
    def to_ical(self) -> bytes: ...
    @staticmethod
    def from_ical(ical, timezone: Incomplete | None = None): ...
    @property
    def dt(self): ...

class vWeekday(str):
    week_days: Incomplete
    relative: Incomplete
    params: Parameters
    def __new__(cls, value, encoding="utf-8"): ...
    def to_ical(self) -> bytes: ...
    @classmethod
    def from_ical(cls, ical): ...

class vFrequency(str):
    frequencies: Incomplete
    params: Parameters
    def __new__(cls, value, encoding="utf-8"): ...
    def to_ical(self) -> bytes: ...
    @classmethod
    def from_ical(cls, ical): ...

class vMonth(int):
    leap: bool
    params: Parameters
    def __new__(cls, month: vMonth | str | int) -> Self: ...
    def to_ical(self) -> bytes: ...
    @classmethod
    def from_ical(cls, ical: vMonth | str | int) -> Self: ...

class vSkip(vText, Enum):
    OMIT = "OMIT"
    FORWARD = "FORWARD"
    BACKWARD = "BACKWARD"

    def __reduce_ex__(self, proto: Unused) -> tuple[Any, ...]: ...

class vRecur(CaselessDict[Incomplete]):
    frequencies: ClassVar[list[str]]
    canonical_order: ClassVar[tuple[str, ...]]
    types: ClassVar[CaselessDict[_PropType]]
    params: Parameters
    def __init__(self, *args, **kwargs) -> None: ...
    def to_ical(self) -> bytes: ...
    @classmethod
    def parse_type(cls, key, values): ...
    @classmethod
    @overload
    def from_ical(cls, ical: _vRecurT) -> _vRecurT: ...
    @classmethod
    @overload
    def from_ical(cls, ical: str) -> Self: ...

class vTime(TimeBase):
    dt: Incomplete
    params: Parameters
    def __init__(self, *args) -> None: ...
    def to_ical(self) -> bytes: ...
    @staticmethod
    def from_ical(ical): ...

class vUri(str):
    params: Parameters
    def __new__(cls, value, encoding="utf-8"): ...
    def to_ical(self) -> bytes: ...
    @classmethod
    def from_ical(cls, ical): ...

class vGeo:
    latitude: Incomplete
    longitude: Incomplete
    params: Parameters
    def __init__(self, geo) -> None: ...
    def to_ical(self) -> bytes: ...
    @staticmethod
    def from_ical(ical): ...
    def __eq__(self, other): ...

class vUTCOffset:
    ignore_exceptions: bool
    td: Incomplete
    params: Parameters
    def __init__(self, td) -> None: ...
    def to_ical(self) -> bytes: ...
    @classmethod
    def from_ical(cls, ical): ...
    def __eq__(self, other): ...

class vInline(str):
    params: Parameters
    def __new__(cls, value, encoding="utf-8"): ...
    def to_ical(self) -> bytes: ...
    @classmethod
    def from_ical(cls, ical): ...

class TypesFactory(CaselessDict[_PropType]):
    all_types: tuple[_PropType, ...]
    def __init__(self, *args, **kwargs) -> None: ...
    types_map: CaselessDict[str]
    def for_property(self, name: str) -> _PropType: ...
    def to_ical(self, name: str, value) -> bytes: ...
    def from_ical(self, name: str, value): ...
