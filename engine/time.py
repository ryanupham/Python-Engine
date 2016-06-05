class GlobalTimeline:
    __current = 0

    @classmethod
    def elapsed_time(cls) -> int:
        return cls.__current

    @classmethod
    def step(cls) -> None:
        cls.__current += 1


class LocalTimeline:
    def __init__(self, anchor=GlobalTimeline, scale: float=1, paused: bool=False):
        self._paused = False
        self._elapsed = 0
        self._anchor, self._scale = anchor, scale
        self._start = anchor.elapsed_time()

        if paused:
            self.pause()

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

    def resume(self) -> None:
        if self._paused:
            self._start = self._anchor.elapsed_time()
            self._paused = False

    def _elapsed_scale(self) -> float:
        return 0 if self._paused else (self._anchor.elapsed_time() - self._start) * self._scale

    def elapsed_time(self) -> float:
        return self._elapsed_scale() + self._elapsed
