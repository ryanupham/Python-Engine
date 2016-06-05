import pyglet

import engine.event_handling as handlers
import engine.entity as entity
from engine.events import EventManager, EventType, StepEvent, DrawEvent
from engine.time import GlobalTimeline


class Game:
    __entities = {}
    __window = pyglet.window.Window()
    __window.set_visible(False)
    __running = False
    steps_per_second = 60

    @classmethod
    def add_entity(cls, ent, position=None):
        if isinstance(ent, entity.Entity):
            if ent.guid not in cls.__entities:
                if position is not None:
                    ent.position = position

                cls.__entities[ent.guid] = ent
        elif isinstance(ent, entity.EntityModel):
            ent = entity.Entity(model=ent, position=position)
            cls.__entities[ent.guid] = ent

    @classmethod
    def remove_entity(cls, ent):
        if isinstance(ent, entity.Entity):
            del cls.__entities[ent.guid]
        elif isinstance(ent, entity.GUID):
            del cls.__entities[ent]

    @classmethod
    def get_entity(cls, ent):
        if isinstance(ent, entity.Entity):
            return cls.__entities.get(ent.guid)
        elif isinstance(ent, entity.GUID):
            return cls.__entities.get(ent)

    @classmethod
    def get_entities(cls, model):
        if isinstance(model, entity.EntityModel):
            name = model.name
        elif isinstance(model, str):
            name = model
        else:
            return []

        return [e for e in cls.__entities if e.name == name]

    @classmethod
    def initialize(cls, width=800, height=600):
        EventManager.register_handler(EventType.CREATE, handlers.create_event_handler)
        EventManager.register_handler(EventType.DESTROY, handlers.destroy_event_handler)
        EventManager.register_handler(EventType.COLLISION, handlers.collision_event_handler)
        EventManager.register_handler(EventType.STEP, handlers.step_event_handler)
        EventManager.register_handler(EventType.DRAW, handlers.draw_event_handler)
        EventManager.register_handler(EventType.INPUT, handlers.input_event_handler)

        cls.__window.width = width
        cls.__window.height = height

    @classmethod
    def start(cls):
        cls.__window.set_visible(True)
        cls.__running = True

        pyglet.clock.schedule_interval(cls.__main, 1/cls.steps_per_second)
        pyglet.app.run()

    @classmethod
    def __main(cls, dt):
        if not cls.__running:
            return

        while not EventManager.empty():
            EventManager.handle_all()
            # detect collisions

        GlobalTimeline.step()

        for e in cls.__entities.values():
            EventManager.raise_event(StepEvent(e))

        while not EventManager.empty():
            EventManager.handle_all()
            # detect collisions

        EventManager.begin_draw()
        cls.__window.clear()

        for e in cls.__entities.values():
            EventManager.raise_event(DrawEvent(e))

        EventManager.end_draw()

        while not EventManager.empty():
            EventManager.handle_all()
            # detect collisions

        # handle input

    @classmethod
    def get_instance(cls):
        return cls
