import engine.spatial as spatial
from engine.events import InputType
from engine.spatial import Position


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
    def __init__(self, name, solid=False, sprite=None, visible=True, parents=None, variables=None):
        self.name, self.solid, self.sprite, self.visible = name, solid, sprite, visible
        self.create_script = self.destroy_script = self.step_script = self.draw_script = None
        self.collision_script = {}
        self.input_script = {InputType.KEY_DOWN: {}, InputType.KEY_UP: {}, InputType.MOUSE_DOWN: {},
                             InputType.MOUSE_UP: {}, InputType.MOUSE_MOVE: None}
        self.variables = variables if variables is not None else {}
        self.parents = set(parents) if parents is not None else set()

        for parent in self.parents:
            parent.inherit(self)

    def add_create_script(self, fn):
        self.create_script = fn

    def add_destroy_script(self, fn):
        self.destroy_script = fn

    def add_collision_script(self, fn, other_name):
        self.collision_script[other_name] = fn

    def add_step_script(self, fn):
        self.step_script = fn

    def add_draw_script(self, fn):
        self.draw_script = fn

    def add_input_script(self, fn, input_type, match=None):
        if input_type == InputType.MOUSE_MOVE:
            self.input_script[input_type] = fn
        else:
            self.input_script[input_type][match] = fn

    def inherit(self, child):
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

    def destroy(self):
        pass


class Entity:
    def __init__(self, model=None, name=None, position=None, solid=False, sprite=None, visible=True):
        self.guid = GUID()

        if position is None:
            position = Position()

        if model is not None:
            self.name, self.position, self.solid, self.sprite, self.visible = model.name, position, model.solid, \
                model.sprite, model.visible
        else:
            self.name, self.position, self.solid, self.sprite, self.visible = name, position, solid, sprite, visible

    def __eq__(self, other):
        return self.guid == other.guid

    def __ne__(self, other):
        return not self.__eq__(other)

    def draw(self):
        if self.visible and self.sprite is not None:
            pass  # TODO: draw self

    def move(self):
        self.position.step()
