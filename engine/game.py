from typing import List, Union

import pyglet

import engine.entity
import engine.event_handlers as handlers
import engine.events
import engine.physics
import engine.spatial
import engine.time


class Game:
    __entities = {}
    __window = pyglet.window.Window(width=1280, height=768)
    __window.set_visible(False)
    __running = False
    __bg_color = (0, 0, 0)
    steps_per_second = 60

    @classmethod
    def add_entity(cls, ent: Union[engine.entity.Entity, engine.entity.EntityModel], position: engine.spatial.Position=None) -> None:
        if isinstance(ent, engine.entity.Entity):
            if ent.guid not in cls.__entities:
                if position is not None:
                    ent.position = position

                cls.__entities[ent.guid] = ent
        elif isinstance(ent, engine.entity.EntityModel):
            ent = engine.entity.Entity(model=ent, position=position)
            cls.__entities[ent.guid] = ent
        else:
            return

        engine.events.EventManager.raise_event(engine.events.CreateEvent(ent, position))

    @classmethod
    def remove_entity(cls, ent: Union[engine.entity.Entity, engine.entity.GUID]) -> None:
        if isinstance(ent, engine.entity.Entity):
            del cls.__entities[ent.guid]
        elif isinstance(ent, engine.entity.GUID):
            del cls.__entities[ent]

    @classmethod
    def get_entity(cls, ent: Union[engine.entity.Entity, engine.entity.GUID]) -> engine.entity.Entity:
        if isinstance(ent, engine.entity.Entity):
            return cls.__entities.get(ent.guid)
        elif isinstance(ent, engine.entity.GUID):
            return cls.__entities.get(ent)

    @classmethod
    def get_entities(cls, model: Union[engine.entity.EntityModel, str]) -> List[engine.entity.Entity]:
        if isinstance(model, engine.entity.EntityModel):
            name = model.name
        elif isinstance(model, str):
            name = model
        else:
            return []

        return [e for e in cls.__entities if e.name == name]

    @classmethod
    def initialize(cls, width: int=800, height: int=600, background_color=(0, 0, 0)) -> None:
        engine.events.EventManager.register_handler(engine.events.CreateEvent, handlers.create_event_handler)
        engine.events.EventManager.register_handler(engine.events.DestroyEvent, handlers.destroy_event_handler)
        engine.events.EventManager.register_handler(engine.events.CollisionEvent, handlers.collision_event_handler)
        engine.events.EventManager.register_handler(engine.events.StepEvent, handlers.step_event_handler)
        engine.events.EventManager.register_handler(engine.events.DrawEvent, handlers.draw_event_handler)
        engine.events.EventManager.register_handler(engine.events.InputEvent, handlers.input_event_handler)

        cls.__bg_color = background_color
        cls.__window.set_size(width, height)

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

        engine.events.EventManager.handle_all()

        engine.time.GlobalTimeline.step()

        cls._detect_collisions()

        engine.events.EventManager.handle_all()

        engine.events.EventManager.begin_draw()
        cls.__window.clear()
        pyglet.gl.glClearColor(cls.__bg_color[0], cls.__bg_color[1], cls.__bg_color[2], 1)

        for e in cls.__entities.values():
            engine.events.EventManager.raise_event(engine.events.DrawEvent(e))

        engine.events.EventManager.end_draw()

        engine.events.EventManager.handle_all()

        # handle input

    @classmethod
    @__window.event
    def on_key_press(symbol, modifiers):
        for ent in Game.__entities:
            engine.events.EventManager.raise_event(engine.events.InputEvent(ent, engine.events.InputType.KEY_DOWN,
                                                                            symbol))

    @classmethod
    @__window.event
    def on_key_release(symbol, modifiers):
        for ent in Game.__entities:
            engine.events.EventManager.raise_event(engine.events.InputEvent(ent, engine.events.InputType.KEY_UP,
                                                                            symbol))
