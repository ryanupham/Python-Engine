import engine.time as time


class MetaEnum(type):
    def __iter__(self):
        for attr in dir(InputType):
            if not attr.startswith("_"):
                yield getattr(self, attr)


class EventType(metaclass=MetaEnum):
    CREATE, DESTROY, COLLISION, STEP, DRAW, INPUT = range(6)


class InputType(metaclass=MetaEnum):
    KEY_DOWN, KEY_UP, MOUSE_DOWN, MOUSE_UP, MOUSE_MOVE = range(5)


class MouseButton:
    LEFT, RIGHT, MIDDLE = range(3)


class Priority:
    def __init__(self, type, anchor=time.GlobalTimeline, delay=0):
        self.type, self.anchor, self.delay = type, anchor, delay
        self.alarm = anchor.elapsed_time() + delay

    def __lt__(self, other):
        if self.anchor.elapsed_time() - self.alarm > other.anchor.elapsed_time() - other.alarm:
            return True

        return self.ready() and self.type < other.type

    def __eq__(self, other):
        return self.ready() == other.ready() and self.type == other.type

    def priority(self):
        return self.alarm * 100 + self.type if self.ready() else -1

    def ready(self):
        return self.anchor.elapsed_time() >= self.alarm

    def __str__(self):
        return str(self.type) + ", " + str(self.delay) + ", " + str(self.ready())


class EventQueue:
    def __init__(self, events=None):
        self._events = sorted(list(events)) if events is not None else []

    def empty(self):
        if len(self._events) == 0:
            return True

        self._events.sort()
        return not self._events[0].ready()

    def get(self):
        if self.empty():
            return None

        return self._events.pop(0)

    def put(self, event):
        self._events.append(event)


class EventManager:
    __queue = EventQueue()

    @classmethod
    def raise_event(cls, event):
        cls.__queue.put(event)

    @classmethod
    def handle_next(cls):
        if not cls.__queue.empty():
            pass

    @classmethod
    def handle_all(cls):
        while not cls.__queue.empty():
            cls.handle_next()


class Event:
    def __init__(self, priority):
        self.priority = priority

    def __lt__(self, other):
        return self.priority < other.priority

    def __eq__(self, other):
        return self.priority == other.priority

    def ready(self):
        return self.priority.ready()


class CreateEvent(Event):
    def __init__(self, entity, position, priority):
        super(CreateEvent, self).__init__(priority)
        self.entity, self.position = entity, position


class DestroyEvent(Event):
    def __init__(self, entity, priority):
        super(DestroyEvent, self).__init__(priority)
        self.entity = entity


class CollisionEvent(Event):
    def __init__(self, entity, other, priority):
        super(CollisionEvent, self).__init__(priority)
        self.entity, self.other = entity, other


class StepEvent(Event):
    def __init__(self, entity, priority):
        super(StepEvent, self).__init__(priority)
        self.entity = entity


class DrawEvent(Event):
    def __init__(self, entity, priority):
        super(DrawEvent, self).__init__(priority)
        self.entity = entity


class InputEvent(Event):
    def __init__(self, entity, input_type, data, priority):
        super(InputEvent, self).__init__(priority)
        self.entity, self.input_type, self.data = entity, input_type, data
