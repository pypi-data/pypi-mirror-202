import abc
import logging
import random
import time
from collections import deque
from typing import (NamedTuple, Optional, Callable, Sequence, Dict,
                    Any, Union, Deque, Set)

import zmq

from zmqbus import Connection, Message

logger = logging.getLogger(__name__)


class DeviceParams(NamedTuple):
    context: zmq.Context[Any] = zmq.Context.instance()
    timeout: float = 5_000
    keepalive_secs: float = 0

    def get_context(self) -> zmq.Context[Any]:
        return self.context or zmq.Context.instance()


class Device(abc.ABC):
    @classmethod
    def get_default_name(cls) -> str:
        return f'{cls.__module__}.{cls.__name__}'

    @property
    def _default_name(self) -> str:
        return self.__class__.get_default_name()

    def __init__(self, name: Optional[str] = None,
                 params: Optional[DeviceParams] = None):
        self._name = name or self._default_name
        self._params = params or DeviceParams()

    @property
    def name(self) -> str:
        return self._name

    def init(self, conn: Connection) -> None:
        pass

    def done(self, conn: Connection) -> None:
        pass

    @abc.abstractmethod
    def run(self, conn: Connection) -> None:
        pass

    def __call__(self,
                 address: str,
                 authkey: bytes,
                 *args: Any,
                 **kwargs: Any) -> None:
        conn = Connection(address=address,
                          authkey=authkey,
                          name=self._name,
                          context=self._params.get_context(),
                          timeout=self._params.timeout,
                          keepalive_secs=self._params.keepalive_secs)
        with conn:
            self.init(conn)
            self.run(conn, *args, **kwargs)
            self.done(conn)


class Pulse(Device):
    def __init__(self,  # pylint: disable=too-many-arguments
                 name: Optional[str] = None,
                 topic: Optional[str] = None,
                 to: Union[str, Sequence[str], None] = None,
                 wait_secs: float = 1,
                 jitter: float = 0,
                 params: Optional[DeviceParams] = None):
        super().__init__(name, params)
        if wait_secs <= 0:
            raise ValueError('Wait must be greater than zero, '
                             f'got {wait_secs}')
        if not (1 > jitter >= 0):  # pylint: disable=superfluous-parens
            raise ValueError('Jitter must be greater or equal to zero '
                             f'and less than one, got {jitter}')
        self._topic = topic or self.name
        self._to = to
        self._wait_secs = wait_secs
        self._jitter = jitter

    def run(self, conn: Connection) -> None:
        i = 1
        while conn.is_alive():
            conn.send(self._topic, to=self._to, payload=i)
            wait_secs = self._wait_secs
            if self._jitter:
                wait_secs *= 1 + self._jitter - (random.random()
                                                 * self._jitter * 2)
            try:
                conn.sleep(wait_secs)
            except BrokenPipeError:
                break
            i += 1

        logger.debug('%r exiting', self.name)


class ScheduledMessage(NamedTuple):
    secs: float
    topic: str
    payload: Optional[Any] = None
    to: Union[str, Sequence[str], None] = None


class Scheduler(Device):
    def __init__(self,  # pylint: disable=too-many-arguments
                 name: Optional[str] = None,
                 messages: Optional[Sequence[ScheduledMessage]] = None,
                 before: Optional[Callable[[Connection], None]] = None,
                 after: Optional[Callable[[Connection], None]] = None,
                 params: Optional[DeviceParams] = None):
        super().__init__(name, params)
        self._messages = messages or ()
        self._before = before
        self._after = after

    def init(self, conn: Connection) -> None:
        if self._before:
            self._before(conn)

    def done(self, conn: Connection) -> None:
        if self._after:
            self._after(conn)

    def run(self, conn: Connection) -> None:
        for smsg in self._messages:
            try:
                conn.sleep(smsg.secs)
                conn.send(smsg.topic, smsg.payload, to=smsg.to)
            except BrokenPipeError:
                break


class ClockParams(NamedTuple):
    topic: str
    secs: float


class Clock(Device):
    def __init__(self,  # pylint: disable=too-many-arguments
                 name: Optional[str] = None,
                 topic: Optional[str] = None,
                 secs: float = 1,
                 to: Union[str, Sequence[str], None] = None,
                 params: Optional[DeviceParams] = None):
        super().__init__(name, params)
        if secs <= 0:
            raise ValueError('Wait must be greater than zero, '
                             f'got {secs}')
        self._topic = topic or self.name
        self._secs = secs
        self._to = to

    def init(self, conn: Connection) -> None:
        conn.add_endpoint('get_params',
                          lambda _conn: ClockParams(topic=self._topic,
                                                    secs=self._secs))

    def run(self, conn: Connection) -> None:
        while conn.is_alive():
            try:
                conn.send(self._topic, time.time(), to=self._to)
                conn.sleep(self._secs)
            except BrokenPipeError:
                break


class PerfMeterPayload(NamedTuple):
    clock: str
    samples: int
    avg_ms: float


class PerfMeter(Device):
    def __init__(self,  # pylint: disable=too-many-arguments
                 name: Optional[str] = None,
                 topic: Optional[str] = None,
                 sender: Optional[str] = None,
                 samples: int = 30,
                 pub_freq: Optional[int] = None,
                 params: Optional[DeviceParams] = None):
        super().__init__(name, params)
        if samples <= 0:
            raise ValueError('Samples must be greater than zero, '
                             f'got {samples}')
        if pub_freq is not None and pub_freq <= 0:
            raise ValueError('Log frequency must be greater than zero, '
                             f'got {pub_freq}')
        self._clock = sender or Clock.get_default_name()
        self._topic = topic or self._name
        self._samples = samples
        self._pub_freq = pub_freq or self._samples

    def _get_clock_params(self, conn: Connection) -> ClockParams:
        while True:
            try:
                req = conn.request(self._clock, 'get_params')
                return conn.response(req)  # type: ignore[no-any-return]
            except TimeoutError:
                logger.warning("'%s.get_params' request timed out",
                               self._clock)

    def run(self, conn: Connection) -> None:

        try:
            params = self._get_clock_params(conn)
        except BrokenPipeError:
            return

        logger.info('Measuring from clock %r posting %r '
                    'at %.1f Hz over %d samples',
                    self._clock, params.topic, params.secs, self._samples)

        try:
            conn.subscribe(params.topic)
            self._run(conn, params.secs)
        except BrokenPipeError:
            pass

        logger.debug('%r exiting', self.name)

    def _run(self, conn: Connection, secs: float) -> None:
        last = -1
        samples: Deque[int] = deque()

        sample_count = 0

        while conn.is_alive():
            msg = conn.recv()

            assert msg.sender == self._clock

            if last > 0:
                nr_samples = len(samples)
                samples.append((msg.payload - last - secs) * 1_000)
                if nr_samples >= self._samples:
                    assert nr_samples == self._samples
                    avg_ms = sum(samples) / self._samples
                    if (sample_count % self._pub_freq) == 0:
                        conn.send(self._topic,
                                  PerfMeterPayload(clock=self._clock,
                                                   samples=sample_count,
                                                   avg_ms=avg_ms))
                    samples.popleft()
                elif (nr_samples % 10) == 0:
                    logger.info('Waiting %d samples, got %d so far',
                                self._samples, nr_samples)
                sample_count += 1

            last = msg.payload


class Dispatcher(Device):
    def __init__(self, name: Optional[str] = None,
                 params: Optional[DeviceParams] = None):
        super().__init__(name, params)
        self._callbacks: Dict[str,
                              Set[Callable[[Connection, Message], None]]] = {}
        self._conn: Optional[Connection] = None

    def _check_connection(self) -> None:
        if not self._conn:
            raise RuntimeError('{self.name!r} is not running')

    def _init_callbacks(self) -> None:
        logger.warning('No callbacks defined by %r (%s.%s)',
                       self.name, self.__module__, self.__class__.__name__)

    def add_callback(self,
                     topic: str,
                     callback: Callable[[Connection, Message], None]) -> None:
        self._check_connection()
        try:
            if callback in self._callbacks[topic]:
                raise ValueError(f'{callback} already set for {topic!r}')
        except KeyError:
            self._callbacks[topic] = set()
            assert self._conn
            self._conn.subscribe(topic)
        self._callbacks[topic].add(callback)

    def remove_callback(self,
                        topic: str,
                        callback: Callable[[Connection, Message],
                                           None]) -> None:
        self._callbacks[topic].remove(callback)
        if not self._callbacks[topic]:
            assert self._conn
            self._conn.unsubscribe(topic)
            del self._callbacks[topic]

    def clear_callbacks(self) -> None:
        if self._conn and self._conn.is_alive():
            try:
                for topic in self._callbacks:
                    self._conn.unsubscribe(topic)
            except BrokenPipeError:
                pass
        self._callbacks.clear()

    def init(self, conn: Connection) -> None:
        self._conn = conn
        self._init_callbacks()

    def done(self, conn: Connection) -> None:
        if self._conn:
            self.clear_callbacks()
            self._conn = None

    def run(self, conn: Connection) -> None:
        while conn.is_alive():
            try:
                msg = conn.recv()
            except BrokenPipeError:
                break
            for topic, callbacks in self._callbacks.items():
                if msg.topic.startswith(topic):
                    for callback in callbacks:
                        if not conn.is_alive():
                            break
                        callback(conn, msg)
                if not conn.is_alive():
                    break
