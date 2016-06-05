from typing import Callable

import pyglet

import engine.events
import engine.spatial
import engine.time


class GUID:
    __counter = 0

    def __init__(self):
        self.__id = GUID.__counter
        GUID.__counter += 1

    def __int__(self):
        return self.__id

    def __str__(self):
        return str(self.__id)

    def __eq__(self, other):
        return int(self) == int(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return self.__id


class EntityModel:
    def __init__(self, name: str, solid: bool = False, sprite: pyglet.sprite.Sprite = None, visible: bool = True,
                 parents=None, variables: dict=None, timeline=engine.time.GlobalTimeline):
        self.name, self.solid, self.sprite, self.visible = name, solid, sprite, visible
        self.create_script = self.destroy_script = self.step_script = self.draw_script = None
        self.collision_script = {}
        self.input_script = {engine.events.InputType.KEY_DOWN: {}, engine.events.InputType.KEY_UP: {},
                             engine.events.InputType.MOUSE_DOWN: {}, engine.events.InputType.MOUSE_UP: {},
                             engine.events.InputType.MOUSE_MOVE: None}
        self.variables = variables if variables is not None else {}
        self.parents = set(parents) if parents is not None else set()
        self.timeline = timeline

        for parent in self.parents:
            parent.inherit(self)

    def add_create_script(self, fn: Callable) -> None:
        self.create_script = fn

    def add_destroy_script(self, fn: Callable) -> None:
        self.destroy_script = fn

    def add_collision_script(self, fn, other_name: str) -> None:
        self.collision_script[other_name] = fn

    def add_step_script(self, fn: Callable) -> None:
        self.step_script = fn

    def add_draw_script(self, fn: Callable) -> None:
        self.draw_script = fn

    def add_input_script(self, fn: Callable, input_type: int, match: int = None) -> None:
        if input_type == engine.events.InputType.MOUSE_MOVE:
            self.input_script[input_type] = fn
        else:
            self.input_script[input_type][match] = fn

    def inherit(self, child) -> None:
        child.variables = dict(self.variables, **child.variables)
        child.collision_script = dict(self.collision_script, **child.collision_script)
        child.create_script = child.create_script if child.create_script is not None else self.create_script
        child.destroy_script = child.destroy_script if child.destroy_script is not None else self.destroy_script
        child.step_script = child.step_script if child.step_script is not None else self.step_script
        child.draw_script = child.draw_script if child.draw_script is not None else self.draw_script
        for in_type in child.input_script:
            if isinstance(child.input_script[in_type], dict):
                child.input_script[in_type] = dict(self.input_script[in_type], **child.input_script[in_type])
            else:
                child.input_script[in_type] = child.input_script[in_type] if child.input_script[in_type] is not None \
                    else self.input_script[in_type]


class Entity:
    def __init__(self, model: EntityModel = None, name: str = None, position: engine.spatial.Position = None,
                 solid: bool = False, sprite: pyglet.sprite.Sprite = None, visible: bool=True,
                 timeline=engine.time.GlobalTimeline):
        self.guid = GUID()

        if position is None:
            position = engine.spatial.Position()

        if model is not None:
            self.name, self.position, self.solid, self.sprite, self.visible = model.name, position, model.solid, \
                                                                              model.sprite, model.visible

            self.create_script, self.destroy_script, self.step_script, self.draw_script, self.collision_script, \
                self.input_script = model.create_script, model.destroy_script, model.step_script, model.draw_script, \
                model.collision_script, model.input_script

            self.variables, self.parents, self.timeline = model.variables, model.parents, model.timeline
        else:
            self.name, self.position, self.solid, self.sprite, self.visible = name, position, solid, sprite, visible

            self.create_script = self.destroy_script = self.step_script = self.draw_script = self.collision_script = \
                self.input_script = None
            self.collision_script = {}
            self.input_script = {engine.events.InputType.KEY_DOWN: {}, engine.events.InputType.KEY_UP: {},
                                 engine.events.InputType.MOUSE_DOWN: {}, engine.events.InputType.MOUSE_UP: {},
                                 engine.events.InputType.MOUSE_MOVE: None}

            self.variables = {}
            self.parents = set()
            self.timeline = timeline

        self.timeline.register(self)

    def destroy(self) -> None:
        engine.events.EventManager.raise_event(engine.events.DestroyEvent(self))

    @property
    def width(self) -> float:
        return self.sprite.width if self.sprite is not None else 0

    @property
    def height(self) -> float:
        return self.sprite.height if self.sprite is not None else 0

    @property
    def x(self) -> float:
        return self.position.x

    @property
    def y(self) -> float:
        return self.position.y

    def __eq__(self, other):
        return self.guid == other.guid

    def __ne__(self, other):
        return not self.__eq__(other)
