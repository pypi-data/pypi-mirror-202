from asyncio import FIRST_COMPLETED, CancelledError, Event, Future, create_task, wait
from dataclasses import dataclass
from typing import AsyncIterator, Generic, Tuple, TypeVar

from option_and_result import NONE, Option, Some

T = TypeVar("T")


@dataclass
class MutableContainer(Generic[T]):
    value: T


@dataclass
class Request(Generic[T]):
    _future: Future[T]

    def fulfill(self, value: T):
        self._future.set_result(value)


@dataclass
class Responder(Generic[T]):
    _shared_future: MutableContainer[Future[Future[T]]]
    _closed: Event
    _disconnected: Event

    async def wait_for_poll(self) -> Option[Request[T]]:
        disconnected_event = create_task(self._disconnected.wait())
        get_task = create_task(wait_for_future(self._shared_future.value))
        try:
            done, _pending = await wait(
                [get_task, disconnected_event], return_when=FIRST_COMPLETED
            )
        except CancelledError:
            disconnected_event.cancel()
            get_task.cancel()
            raise

        if disconnected_event in done:
            get_task.cancel()
            return NONE()

        assert get_task in done
        disconnected_event.cancel()
        if self._closed.is_set():
            self._disconnected.set()

        return Some(Request(get_task.result()))

    async def __aiter__(self) -> AsyncIterator[Request[T]]:
        while True:
            received = await self.wait_for_poll()

            if received.is_none():
                return

            yield received.unwrap()

    def close(self):
        self._closed.set()
        self._disconnected.set()

    def __del__(self):
        self.close()


@dataclass
class Response(Generic[T]):
    _future: Future[T]

    def __await__(self):
        return self._future.__await__()


async def wait_for_future(future: Future[T]) -> T:
    return await future


@dataclass
class Requester(Generic[T]):
    _shared_future: MutableContainer[Future[Future[T]]]
    _closed: Event
    _disconnected: Event
    _waiters: int

    async def request(self) -> Option[Response[T]]:
        if self._waiters == 0:
            self._shared_future.value.set_result(Future())

        self._waiters += 1

        disconnected_event = create_task(self._disconnected.wait())
        get_task = create_task(wait_for_future(self._shared_future.value))
        try:
            done, _pending = await wait(
                [get_task, disconnected_event], return_when=FIRST_COMPLETED
            )
        except CancelledError:
            disconnected_event.cancel()
            get_task.cancel()
            self._waiters -= 1
            raise

        if disconnected_event in done:
            get_task.cancel()
            self._waiters -= 1
            return NONE()

        assert get_task in done
        disconnected_event.cancel()
        if self._closed.is_set():
            self._disconnected.set()

        self._waiters -= 1

        if self._waiters == 0:
            self._shared_future.value = Future()

        return Some(Response(get_task.result()))

    async def request_and_wait(self) -> Option[T]:
        future_option = await self.request()

        if future_option.is_none():
            return NONE()

        future = future_option.unwrap()
        result = await future
        return Some(result)

    async def __aiter__(self) -> AsyncIterator[T]:
        while True:
            received = await self.request_and_wait()

            if received.is_none():
                return

            yield received.unwrap()

    def close(self):
        self._closed.set()
        if not self._shared_future.value.done():
            self._disconnected.set()

    def __del__(self):
        self.close()


def coordinator() -> Tuple[Responder[T], Requester[T]]:
    shared_future: MutableContainer[Future[Future[T]]] = MutableContainer(Future())
    closed = Event()
    disconnected = Event()

    responder = Responder(
        _shared_future=shared_future,
        _closed=closed,
        _disconnected=disconnected,
    )
    requester = Requester(
        _shared_future=shared_future,
        _closed=closed,
        _disconnected=disconnected,
        _waiters=0,
    )

    return (responder, requester)
