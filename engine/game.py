from typing import TypeVar, List

import pyglet

import engine.entity as entity
import engine.event_handlers as handlers
import engine.events
import engine.physics
import engine.spatial
import engine.time


AnyEntity = TypeVar("AnyEntity", entity.Entity, entity.EntityModel)
EntityID = TypeVar("EntityID", entity.Entity, entity.GUID)
ModelID = TypeVar("ModelID", entity.EntityModel, str)


class Game:
    __entities = {}
    __window = pyglet.window.Window()
    __window.set_visible(False)
    __running = False
    steps_per_second = 60

    @classmethod
    def add_entity(cls, ent: AnyEntity, position: engine.spatial.Position=None) -> None:
        if isinstance(ent, entity.Entity):
            if ent.guid not in cls.__entities:
                if position is not None:
                    ent.position = position

                cls.__entities[ent.guid] = ent
        elif isinstance(ent, entity.EntityModel):
            ent = entity.Entity(model=ent, position=position)
            cls.__entities[ent.guid] = ent
        else:
            return

        engine.events.EventManager.raise_event(engine.events.CreateEvent(ent, position))

    @classmethod
    def remove_entity(cls, ent: EntityID) -> None:
        if isinstance(ent, entity.Entity):
            del cls.__entities[ent.guid]
        elif isinstance(ent, entity.GUID):
            del cls.__entities[ent]

    @classmethod
    def get_entity(cls, ent: EntityID) -> entity.Entity:
        if isinstance(ent, entity.Entity):
            return cls.__entities.get(ent.guid)
        elif isinstance(ent, entity.GUID):
            return cls.__entities.get(ent)

    @classmethod
    def get_entities(cls, model: ModelID) -> List[entity.Entity]:
        if isinstance(model, entity.EntityModel):
            name = model.name
        elif isinstance(model, str):
            name = model
        else:
            return []

        return [e for e in cls.__entities if e.name == name]

    @classmethod
    def initialize(cls, width: int=800, height: int=600) -> None:
        engine.events.EventManager.register_handler(engine.events.CreateEvent, handlers.create_event_handler)
        engine.events.EventManager.register_handler(engine.events.DestroyEvent, handlers.destroy_event_handler)
        engine.events.EventManager.register_handler(engine.events.CollisionEvent, handlers.collision_event_handler)
        engine.events.EventManager.register_handler(engine.events.StepEvent, handlers.step_event_handler)
        engine.events.EventManager.register_handler(engine.events.DrawEvent, handlers.draw_event_handler)
        engine.events.EventManager.register_handler(engine.events.InputEvent, handlers.input_event_handler)

        cls.__window.width = width
        cls.__window.height = height

    @classmethod
    def start(cls) -> None:
        cls.__window.set_visible(True)
        cls.__running = True

        pyglet.clock.schedule_interval(cls.__main, 1/cls.steps_per_second)
        pyglet.app.run()

    @classmethod
    def _detect_collisions(cls):
        for collision in engine.physics.find_collisions(cls.__entities.values()):
            engine.events.EventManager.raise_event(engine.events.CollisionEvent(collision[0], collision[1]))
            engine.events.EventManager.raise_event(engine.events.CollisionEvent(collision[1], collision[0]))

    @classmethod
    def __main(cls, dt) -> None:
        if not cls.__running:
            return

        while not engine.events.EventManager.empty():
            engine.events.EventManager.handle_all()
            cls._detect_collisions()

        engine.time.GlobalTimeline.step()

        for e in cls.__entities.values():
            engine.events.EventManager.raise_event(engine.events.StepEvent(e))

        while not engine.events.EventManager.empty():
            engine.events.EventManager.handle_all()
            cls._detect_collisions()

        engine.events.EventManager.begin_draw()
        cls.__window.clear()

        for e in cls.__entities.values():
            engine.events.EventManager.raise_event(engine.events.DrawEvent(e))

        engine.events.EventManager.end_draw()

        while not engine.events.EventManager.empty():
            engine.events.EventManager.handle_all()
            cls._detect_collisions()

        # handle input
