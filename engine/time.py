from typing import Union

import engine.entity
import engine.events


class GlobalTimeline:
    __current = 0
    __registered_entities = set()
    __registered_timelines = set()

    @classmethod
    def elapsed_time(cls) -> int:
        return cls.__current

    @classmethod
    def step(cls) -> None:
        cls.__current += 1

        for entity in cls.__registered_entities:
            engine.events.EventManager.raise_event(engine.events.StepEvent(entity))

        for timeline in cls.__registered_timelines:
            timeline.alert()

    @classmethod
    def register(cls, ent) -> None:
        if isinstance(ent, engine.entity.Entity):
            cls.__registered_entities.add(ent.guid)
        elif isinstance(ent, engine.entity.GUID):
            cls.__registered_entities.add(ent)
        elif isinstance(ent, LocalTimeline):
            cls.__registered_timelines.add(ent)


class LocalTimeline:
    def __init__(self, anchor=GlobalTimeline, scale: float=1, paused: bool=False):
        self._paused = False
        self._elapsed = 0
        self._anchor, self._scale = anchor, scale
        self._start = anchor.elapsed_time()
        self.__registered_entities = set()
        self.__registered_timelines = set()
        self.__last = 0
        self.__count = 0

        if paused:
            self.pause()

        anchor.register(self)

    @property
    def scale(self) -> float:
        return self._scale

    @scale.setter
    def scale(self, val: float) -> None:
        self._elapsed += self._elapsed_scale()
        self._start = self._anchor.elapsed_time()
        self._scale = val

    def pause(self) -> None:
        if not self._paused:
            self._elapsed += self._elapsed_scale()
            self._paused = True

    @property
    def paused(self) -> bool:
        return self._paused

    def resume(self) -> None:
        if self._paused:
            self._start = self._anchor.elapsed_time()
            self._paused = False

    def _elapsed_scale(self) -> float:
        return 0 if self._paused else (self._anchor.elapsed_time() - self._start) * self._scale

    def elapsed_time(self) -> float:
        return self._elapsed_scale() + self._elapsed

    def register(self, ent) -> None:
        if isinstance(ent, engine.entity.Entity):
            self.__registered_entities.add(ent.guid)
        elif isinstance(ent, engine.entity.GUID):
            self.__registered_entities.add(ent)
        elif isinstance(ent, LocalTimeline):
            self.__registered_timelines.add(ent)

    def alert(self) -> None:
        self.__count += self.elapsed_time() - self.__last
        self.__last = self.elapsed_time()

        while self.__count >= 1:
            self.__count -= 1

            for entity in self.__registered_entities:
                engine.events.EventManager.raise_event(
                        engine.events.StepEvent(entity, engine.events.Priority(engine.events.EventType.STEP, self)))

        for timeline in self.__registered_timelines:
            timeline.alert()
