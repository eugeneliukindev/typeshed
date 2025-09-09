import threading
from collections.abc import Callable, Iterable, Set as AbstractSet
from re import Pattern
from typing import TypeAlias, TypedDict, override, type_check_only

COMPILED_EXT_RE: Pattern[str]

class Reloader(threading.Thread):
    daemon: bool

    def __init__(
        self, extra_files: Iterable[str] | None = None, interval: int = 1, callback: Callable[[str], None] | None = None
    ) -> None: ...
    def add_extra_file(self, filename: str) -> None: ...
    def get_files(self) -> list[str]: ...
    @override
    def run(self) -> None: ...

has_inotify: bool

class InotifyReloader(threading.Thread):
    event_mask: int
    daemon: bool

    def __init__(self, extra_files: Iterable[str] | None = None, callback: Callable[[str], None] | None = None) -> None: ...
    def add_extra_file(self, filename: str) -> None: ...
    def get_dirs(self) -> AbstractSet[str]: ...
    @override
    def run(self) -> None: ...

_PreferredReloaderType: TypeAlias = type[InotifyReloader | Reloader]
_ReloaderType: TypeAlias = InotifyReloader | Reloader  # noqa: Y047

@type_check_only
class _ReloadedEngines(TypedDict):
    auto: _PreferredReloaderType
    pool: type[Reloader]
    inotify: type[InotifyReloader]

preferred_reloader: _PreferredReloaderType
reloader_engines: _ReloadedEngines
