from engine.game import Game
from engine.spatial import Position


def create_event_handler(event):
    if event.position is None:
        event.position = Position()

    event.entity.position = event.position

    if event.entity.create_script is not None:
        event.entity.create_script()

    Game.add_entity(event.entity)


def destroy_event_handler(event):
    if event.entity.destroy_script is not None:
        event.entity.destroy_script()

    Game.remove_entity(event.entity)


def collision_event_handler(event):
    if event.entity.collision_script[event.other.name] is not None:
        event.entity.collision_script[event.other.name](event.other)


def step_event_handler(event):
    if event.entity.step_script is not None:
        event.entity.step_script()


def draw_event_handler(event):
    if event.entity.draw_script is not None:
        event.entity.draw_script()
    else:
        pass  # TODO: drawing


def input_event_handler(event):
    if event.input_type in event.entity.input_script:
        if isinstance(event.entity.input_script[event.input_type], dict):
            if event.entity.input_script[event.input_type][event.data] is not None:
                event.entity.input_script[event.input_type][event.data]()
        else:
            if event.entity.input_script[event.input_type] is not None:
                event.entity.input_script[event.input_type]()
