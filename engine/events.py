import engine.time as time


class MetaEnum(type):
    def __iter__(self):
        for attr in dir(InputType):
            if not attr.startswith("_"):
                yield getattr(self, attr)


class EventType(metaclass=MetaEnum):
    GAME_START, CREATE, DESTROY, COLLISION, STEP, DRAW, INPUT = range(7)


class InputType(metaclass=MetaEnum):
    KEY_DOWN, KEY_UP, MOUSE_DOWN, MOUSE_UP, MOUSE_MOVE = range(5)


class MouseButton:
    LEFT, RIGHT, MIDDLE = range(3)


class Priority:
    def __init__(self, event_type=-1, anchor=time.GlobalTimeline, delay=0):
        self.type, self.anchor, self.delay = event_type, anchor, delay
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

    def next(self):
        if self.empty():
            return None

        return self._events.pop(0)

    def put(self, event):
        self._events.append(event)


class EventManager:
    __queue = EventQueue()
    __handlers = {}
    __drawing = False

    @classmethod
    def register_handler(cls, event_type, handler):
        cls.__handlers[event_type] = handler

    @classmethod
    def raise_event(cls, event):
        if not cls.__drawing:
            cls.__queue.put(event)

    @classmethod
    def begin_draw(cls):
        cls.__drawing = True

    @classmethod
    def end_draw(cls):
        cls.__drawing = False

    @classmethod
    def handle_next(cls):
        if not cls.__queue.empty():
            event = cls.__queue.next()

            if type(event) in cls.__handlers:
                cls.__handlers[type(event)](event)

    @classmethod
    def handle_all(cls):
        while not cls.__queue.empty():
            cls.handle_next()

    @classmethod
    def empty(cls):
        return cls.__queue.empty()


class Event:
    def __init__(self, priority):
        self.priority = priority

    def __lt__(self, other):
        return self.priority < other.priority

    def __eq__(self, other):
        return self.priority == other.priority

    def ready(self):
        return self.priority.ready()


class GameStartEvent(Event):
    def __init__(self, priority=Priority()):
        priority.type = EventType.GAME_START
        super(GameStartEvent, self).__init__(priority)


class CreateEvent(Event):
    def __init__(self, entity, position, priority=Priority()):
        priority.type = EventType.CREATE
        super(CreateEvent, self).__init__(priority)
        self.entity, self.position = entity, position


class DestroyEvent(Event):
    def __init__(self, entity, priority=Priority()):
        priority.type = EventType.DESTROY
        super(DestroyEvent, self).__init__(priority)
        self.entity = entity


class CollisionEvent(Event):
    def __init__(self, entity, other, priority=Priority()):
        priority.type = EventType.COLLISION
        super(CollisionEvent, self).__init__(priority)
        self.entity, self.other = entity, other


class StepEvent(Event):
    def __init__(self, entity, priority=Priority()):
        priority.type = EventType.STEP
        super(StepEvent, self).__init__(priority)
        self.entity = entity


class DrawEvent(Event):
    def __init__(self, entity, priority=Priority()):
        priority.type = EventType.DRAW
        super(DrawEvent, self).__init__(priority)
        self.entity = entity


class InputEvent(Event):
    def __init__(self, entity, input_type, data, priority=Priority()):
        priority.type = EventType.INPUT
        super(InputEvent, self).__init__(priority)
        self.entity, self.input_type, self.data = entity, input_type, data
