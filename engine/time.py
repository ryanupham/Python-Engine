class GlobalTimeline:
    __current = 0

    @classmethod
    def elapsed_time(cls):
        return cls.__current

    @classmethod
    def step(cls):
        cls.__current += 1


class LocalTimeline:
    def __init__(self, anchor=GlobalTimeline, scale=1, paused=False):
        self._paused = False
        self._elapsed = 0
        self._anchor, self._scale = anchor, scale
        self._start = anchor.elapsed_time()

        if paused:
            self.pause()

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, val):
        self._elapsed += self.elapsed_scale()
        self._start = self._anchor.elapsed_time()
        self._scale = val

    def pause(self):
        if not self._paused:
            self._elapsed += self.elapsed_scale()
            self._paused = True

    def resume(self):
        if self._paused:
            self._start = self._anchor.elapsed_time()
            self._paused = False

    def elapsed_scale(self):
        return 0 if self._paused else (self._anchor.elapsed_time() - self._start) * self._scale

    def elapsed_time(self):
        return self.elapsed_scale() + self._elapsed
