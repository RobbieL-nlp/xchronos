from typing import Callable
from clock.hand import Hour, Minute, Second
from mark import MarkT, SpecT

TimeT = tuple[int, int, int]
MarkF = Callable[[int, int], tuple[int, int]]
ClockF = Callable[[TimeT, int], tuple[TimeT, int]]


class Clock:
    __slots__ = ("_hour", "_minute", "_second")

    def __init__(self, hour: SpecT, mins: SpecT, sec: SpecT) -> None:
        self._hour = Hour(hour)
        self._minute = Minute(mins)
        self._second = Second(sec)

    def _travel(self, now: TimeT, leap: int, fn: str) -> tuple[TimeT, int]:
        h, m, s = now
        func: MarkF = getattr(self._second, fn)
        s, aux = func(s, leap)

        leap = aux + int(m not in self._minute)
        if leap > 0:
            func = getattr(self._minute, fn)
            m, aux = func(m, leap)

        l = aux + int(h not in self._hour)
        if l > 0:
            func = getattr(self._hour, fn)
            h, aux = func(h, l)

        return (h, m, s), aux

    def prev(self, now: TimeT, leap: int = 1):
        return self._travel(now, leap, "prev")

    def next(self, now: TimeT, leap: int = 1):
        return self._travel(now, leap, "next")

    def contains(self, now: TimeT) -> bool:
        return all(
            (
                self._second.contains(now[2]),
                self._minute.contains(now[1]),
                self._hour.contains(now[0]),
            )
        )

    __contains__ = contains