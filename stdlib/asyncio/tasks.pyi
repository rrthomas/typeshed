import concurrent.futures
import sys
from collections.abc import Awaitable, Coroutine, Generator, Iterable, Iterator
from types import FrameType
from typing import Any, Generic, TextIO, TypeVar, overload
from typing_extensions import Literal, TypeAlias

from . import _CoroutineLike
from .events import AbstractEventLoop
from .futures import Future

if sys.version_info >= (3, 9):
    from types import GenericAlias
if sys.version_info >= (3, 11):
    from contextvars import Context

__all__ = (
    "Task",
    "create_task",
    "FIRST_COMPLETED",
    "FIRST_EXCEPTION",
    "ALL_COMPLETED",
    "wait",
    "wait_for",
    "as_completed",
    "sleep",
    "gather",
    "shield",
    "ensure_future",
    "run_coroutine_threadsafe",
    "current_task",
    "all_tasks",
    "_register_task",
    "_unregister_task",
    "_enter_task",
    "_leave_task",
)

_T = TypeVar("_T")
_T_co = TypeVar("_T_co", covariant=True)
_T1 = TypeVar("_T1")
_T2 = TypeVar("_T2")
_T3 = TypeVar("_T3")
_T4 = TypeVar("_T4")
_T5 = TypeVar("_T5")
_FT = TypeVar("_FT", bound=Future[Any])
_FutureLike: TypeAlias = Future[_T] | Generator[Any, None, _T] | Awaitable[_T]
_TaskYieldType: TypeAlias = Future[object] | None

FIRST_COMPLETED = concurrent.futures.FIRST_COMPLETED
FIRST_EXCEPTION = concurrent.futures.FIRST_EXCEPTION
ALL_COMPLETED = concurrent.futures.ALL_COMPLETED

if sys.version_info >= (3, 10):
    def as_completed(fs: Iterable[_FutureLike[_T]], *, timeout: float | None = None) -> Iterator[Future[_T]]: ...

else:
    def as_completed(
        fs: Iterable[_FutureLike[_T]], *, loop: AbstractEventLoop | None = None, timeout: float | None = None
    ) -> Iterator[Future[_T]]: ...

@overload
def ensure_future(coro_or_future: _FT, *, loop: AbstractEventLoop | None = None) -> _FT: ...  # type: ignore[misc]
@overload
def ensure_future(coro_or_future: Awaitable[_T], *, loop: AbstractEventLoop | None = None) -> Task[_T]: ...

# `gather()` actually returns a list with length equal to the number
# of tasks passed; however, Tuple is used similar to the annotation for
# zip() because typing does not support variadic type variables.  See
# typing PR #1550 for discussion.
#
# The many type: ignores here are because the overloads overlap,
# but having overlapping overloads is the only way to get acceptable type inference in all edge cases.
if sys.version_info >= (3, 10):
    @overload
    def gather(__coro_or_future1: _FutureLike[_T1], *, return_exceptions: Literal[False] = False) -> Future[tuple[_T1]]: ...  # type: ignore[misc]
    @overload
    def gather(  # type: ignore[misc]
        __coro_or_future1: _FutureLike[_T1], __coro_or_future2: _FutureLike[_T2], *, return_exceptions: Literal[False] = False
    ) -> Future[tuple[_T1, _T2]]: ...
    @overload
    def gather(  # type: ignore[misc]
        __coro_or_future1: _FutureLike[_T1],
        __coro_or_future2: _FutureLike[_T2],
        __coro_or_future3: _FutureLike[_T3],
        *,
        return_exceptions: Literal[False] = False,
    ) -> Future[tuple[_T1, _T2, _T3]]: ...
    @overload
    def gather(  # type: ignore[misc]
        __coro_or_future1: _FutureLike[_T1],
        __coro_or_future2: _FutureLike[_T2],
        __coro_or_future3: _FutureLike[_T3],
        __coro_or_future4: _FutureLike[_T4],
        *,
        return_exceptions: Literal[False] = False,
    ) -> Future[tuple[_T1, _T2, _T3, _T4]]: ...
    @overload
    def gather(  # type: ignore[misc]
        __coro_or_future1: _FutureLike[_T1],
        __coro_or_future2: _FutureLike[_T2],
        __coro_or_future3: _FutureLike[_T3],
        __coro_or_future4: _FutureLike[_T4],
        __coro_or_future5: _FutureLike[_T5],
        *,
        return_exceptions: Literal[False] = False,
    ) -> Future[tuple[_T1, _T2, _T3, _T4, _T5]]: ...
    @overload
    def gather(__coro_or_future1: _FutureLike[_T1], *, return_exceptions: bool) -> Future[tuple[_T1 | BaseException]]: ...  # type: ignore[misc]
    @overload
    def gather(  # type: ignore[misc]
        __coro_or_future1: _FutureLike[_T1], __coro_or_future2: _FutureLike[_T2], *, return_exceptions: bool
    ) -> Future[tuple[_T1 | BaseException, _T2 | BaseException]]: ...
    @overload
    def gather(  # type: ignore[misc]
        __coro_or_future1: _FutureLike[_T1],
        __coro_or_future2: _FutureLike[_T2],
        __coro_or_future3: _FutureLike[_T3],
        *,
        return_exceptions: bool,
    ) -> Future[tuple[_T1 | BaseException, _T2 | BaseException, _T3 | BaseException]]: ...
    @overload
    def gather(  # type: ignore[misc]
        __coro_or_future1: _FutureLike[_T1],
        __coro_or_future2: _FutureLike[_T2],
        __coro_or_future3: _FutureLike[_T3],
        __coro_or_future4: _FutureLike[_T4],
        *,
        return_exceptions: bool,
    ) -> Future[tuple[_T1 | BaseException, _T2 | BaseException, _T3 | BaseException, _T4 | BaseException]]: ...
    @overload
    def gather(  # type: ignore[misc]
        __coro_or_future1: _FutureLike[_T1],
        __coro_or_future2: _FutureLike[_T2],
        __coro_or_future3: _FutureLike[_T3],
        __coro_or_future4: _FutureLike[_T4],
        __coro_or_future5: _FutureLike[_T5],
        *,
        return_exceptions: bool,
    ) -> Future[
        tuple[_T1 | BaseException, _T2 | BaseException, _T3 | BaseException, _T4 | BaseException, _T5 | BaseException]
    ]: ...
    @overload
    def gather(*coros_or_futures: _FutureLike[Any], return_exceptions: bool = False) -> Future[list[Any]]: ...

else:
    @overload
    def gather(  # type: ignore[misc]
        __coro_or_future1: _FutureLike[_T1], *, loop: AbstractEventLoop | None = None, return_exceptions: Literal[False] = False
    ) -> Future[tuple[_T1]]: ...
    @overload
    def gather(  # type: ignore[misc]
        __coro_or_future1: _FutureLike[_T1],
        __coro_or_future2: _FutureLike[_T2],
        *,
        loop: AbstractEventLoop | None = None,
        return_exceptions: Literal[False] = False,
    ) -> Future[tuple[_T1, _T2]]: ...
    @overload
    def gather(  # type: ignore[misc]
        __coro_or_future1: _FutureLike[_T1],
        __coro_or_future2: _FutureLike[_T2],
        __coro_or_future3: _FutureLike[_T3],
        *,
        loop: AbstractEventLoop | None = None,
        return_exceptions: Literal[False] = False,
    ) -> Future[tuple[_T1, _T2, _T3]]: ...
    @overload
    def gather(  # type: ignore[misc]
        __coro_or_future1: _FutureLike[_T1],
        __coro_or_future2: _FutureLike[_T2],
        __coro_or_future3: _FutureLike[_T3],
        __coro_or_future4: _FutureLike[_T4],
        *,
        loop: AbstractEventLoop | None = None,
        return_exceptions: Literal[False] = False,
    ) -> Future[tuple[_T1, _T2, _T3, _T4]]: ...
    @overload
    def gather(  # type: ignore[misc]
        __coro_or_future1: _FutureLike[_T1],
        __coro_or_future2: _FutureLike[_T2],
        __coro_or_future3: _FutureLike[_T3],
        __coro_or_future4: _FutureLike[_T4],
        __coro_or_future5: _FutureLike[_T5],
        *,
        loop: AbstractEventLoop | None = None,
        return_exceptions: Literal[False] = False,
    ) -> Future[tuple[_T1, _T2, _T3, _T4, _T5]]: ...
    @overload
    def gather(  # type: ignore[misc]
        __coro_or_future1: _FutureLike[_T1], *, loop: AbstractEventLoop | None = None, return_exceptions: bool
    ) -> Future[tuple[_T1 | BaseException]]: ...
    @overload
    def gather(  # type: ignore[misc]
        __coro_or_future1: _FutureLike[_T1],
        __coro_or_future2: _FutureLike[_T2],
        *,
        loop: AbstractEventLoop | None = None,
        return_exceptions: bool,
    ) -> Future[tuple[_T1 | BaseException, _T2 | BaseException]]: ...
    @overload
    def gather(  # type: ignore[misc]
        __coro_or_future1: _FutureLike[_T1],
        __coro_or_future2: _FutureLike[_T2],
        __coro_or_future3: _FutureLike[_T3],
        *,
        loop: AbstractEventLoop | None = None,
        return_exceptions: bool,
    ) -> Future[tuple[_T1 | BaseException, _T2 | BaseException, _T3 | BaseException]]: ...
    @overload
    def gather(  # type: ignore[misc]
        __coro_or_future1: _FutureLike[_T1],
        __coro_or_future2: _FutureLike[_T2],
        __coro_or_future3: _FutureLike[_T3],
        __coro_or_future4: _FutureLike[_T4],
        *,
        loop: AbstractEventLoop | None = None,
        return_exceptions: bool,
    ) -> Future[tuple[_T1 | BaseException, _T2 | BaseException, _T3 | BaseException, _T4 | BaseException]]: ...
    @overload
    def gather(  # type: ignore[misc]
        __coro_or_future1: _FutureLike[_T1],
        __coro_or_future2: _FutureLike[_T2],
        __coro_or_future3: _FutureLike[_T3],
        __coro_or_future4: _FutureLike[_T4],
        __coro_or_future5: _FutureLike[_T5],
        *,
        loop: AbstractEventLoop | None = None,
        return_exceptions: bool,
    ) -> Future[
        tuple[_T1 | BaseException, _T2 | BaseException, _T3 | BaseException, _T4 | BaseException, _T5 | BaseException]
    ]: ...
    @overload
    def gather(
        *coros_or_futures: _FutureLike[Any], loop: AbstractEventLoop | None = None, return_exceptions: bool = False
    ) -> Future[list[Any]]: ...

def run_coroutine_threadsafe(coro: _FutureLike[_T], loop: AbstractEventLoop) -> concurrent.futures.Future[_T]: ...

if sys.version_info >= (3, 10):
    def shield(arg: _FutureLike[_T]) -> Future[_T]: ...
    @overload
    async def sleep(delay: float) -> None: ...
    @overload
    async def sleep(delay: float, result: _T) -> _T: ...
    @overload
    async def wait(fs: Iterable[_FT], *, timeout: float | None = None, return_when: str = "ALL_COMPLETED") -> tuple[set[_FT], set[_FT]]: ...  # type: ignore[misc]
    @overload
    async def wait(
        fs: Iterable[Awaitable[_T]], *, timeout: float | None = None, return_when: str = "ALL_COMPLETED"
    ) -> tuple[set[Task[_T]], set[Task[_T]]]: ...
    async def wait_for(fut: _FutureLike[_T], timeout: float | None) -> _T: ...

else:
    def shield(arg: _FutureLike[_T], *, loop: AbstractEventLoop | None = None) -> Future[_T]: ...
    @overload
    async def sleep(delay: float, *, loop: AbstractEventLoop | None = None) -> None: ...
    @overload
    async def sleep(delay: float, result: _T, *, loop: AbstractEventLoop | None = None) -> _T: ...
    @overload
    async def wait(  # type: ignore[misc]
        fs: Iterable[_FT],
        *,
        loop: AbstractEventLoop | None = None,
        timeout: float | None = None,
        return_when: str = "ALL_COMPLETED",
    ) -> tuple[set[_FT], set[_FT]]: ...
    @overload
    async def wait(
        fs: Iterable[Awaitable[_T]],
        *,
        loop: AbstractEventLoop | None = None,
        timeout: float | None = None,
        return_when: str = "ALL_COMPLETED",
    ) -> tuple[set[Task[_T]], set[Task[_T]]]: ...
    async def wait_for(fut: _FutureLike[_T], timeout: float | None, *, loop: AbstractEventLoop | None = None) -> _T: ...

if sys.version_info >= (3, 12):
    _TaskCompatibleCoro: TypeAlias = Coroutine[Any, Any, _T_co]
else:
    _TaskCompatibleCoro: TypeAlias = Generator[_TaskYieldType, None, _T_co] | Awaitable[_T_co]

# mypy and pyright complain that a subclass of an invariant class shouldn't be covariant.
# While this is true in general, here it's sort-of okay to have a covariant subclass,
# since the only reason why `asyncio.Future` is invariant is the `set_result()` method,
# and `asyncio.Task.set_result()` always raises.
class Task(Future[_T_co], Generic[_T_co]):  # type: ignore[type-var]  # pyright: ignore[reportGeneralTypeIssues]
    if sys.version_info >= (3, 12):
        def __init__(
            self,
            coro: _TaskCompatibleCoro[_T_co],
            *,
            loop: AbstractEventLoop = ...,
            name: str | None,
            context: Context | None = None,
            eager_start: bool = False,
        ) -> None: ...
    elif sys.version_info >= (3, 11):
        def __init__(
            self,
            coro: _TaskCompatibleCoro[_T_co],
            *,
            loop: AbstractEventLoop = ...,
            name: str | None,
            context: Context | None = None,
        ) -> None: ...
    elif sys.version_info >= (3, 8):
        def __init__(
            self, coro: _TaskCompatibleCoro[_T_co], *, loop: AbstractEventLoop = ..., name: str | None = ...
        ) -> None: ...
    else:
        def __init__(self, coro: _TaskCompatibleCoro[_T_co], *, loop: AbstractEventLoop = ...) -> None: ...
    if sys.version_info >= (3, 8):
        def get_coro(self) -> _TaskCompatibleCoro[_T_co]: ...
        def get_name(self) -> str: ...
        def set_name(self, __value: object) -> None: ...

    def get_stack(self, *, limit: int | None = None) -> list[FrameType]: ...
    def print_stack(self, *, limit: int | None = None, file: TextIO | None = None) -> None: ...
    if sys.version_info >= (3, 11):
        def cancelling(self) -> int: ...
        def uncancel(self) -> int: ...
    if sys.version_info < (3, 9):
        @classmethod
        def current_task(cls, loop: AbstractEventLoop | None = None) -> Task[Any] | None: ...
        @classmethod
        def all_tasks(cls, loop: AbstractEventLoop | None = None) -> set[Task[Any]]: ...
    if sys.version_info >= (3, 9):
        def __class_getitem__(cls, item: Any) -> GenericAlias: ...

def all_tasks(loop: AbstractEventLoop | None = None) -> set[Task[Any]]: ...

if sys.version_info >= (3, 11):
    def create_task(coro: _CoroutineLike[_T], *, name: str | None = None, context: Context | None = None) -> Task[_T]: ...

elif sys.version_info >= (3, 8):
    def create_task(coro: _CoroutineLike[_T], *, name: str | None = None) -> Task[_T]: ...

else:
    def create_task(coro: _CoroutineLike[_T]) -> Task[_T]: ...

def current_task(loop: AbstractEventLoop | None = None) -> Task[Any] | None: ...
def _enter_task(loop: AbstractEventLoop, task: Task[Any]) -> None: ...
def _leave_task(loop: AbstractEventLoop, task: Task[Any]) -> None: ...
def _register_task(task: Task[Any]) -> None: ...
def _unregister_task(task: Task[Any]) -> None: ...
