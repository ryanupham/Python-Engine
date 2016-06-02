import engine.spatial as spatial
from engine.events import InputType


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


class EntityModel:
    def __init__(self, name, solid=False, sprite=None, visible=True):
        self.name, self.solid, self.sprite, self.visible = name, solid, sprite, visible
        self.create_script = self.destroy_script = self.step_script = self.draw_script = None
        self.collision_script = {}
        self.input_script = {InputType.KEY_DOWN: {}, InputType.KEY_UP: {}, InputType.MOUSE_DOWN: {},
                             InputType.MOUSE_UP: {}, InputType.MOUSE_MOVE: None}

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


class Entity:
    def __init__(self, name=None, position=spatial.Position(), solid=False, sprite=None, visible=True):
        self.guid = GUID()

        self.name, self.position, self.solid, self.sprite, self.visible = name, position, solid, sprite, visible

    def __eq__(self, other):
        return self.guid == other.guid

    def __ne__(self, other):
        return not self.__eq__(other)

    def draw(self):
        if self.visible and self.sprite is not None:
            pass

    def move(self):
        self.position.step()
