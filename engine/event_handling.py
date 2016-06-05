import engine.game
from engine.spatial import Position


def create_event_handler(event):
    if event.position is None:
        event.position = Position()

    event.entity.position = event.position

    engine.game.Game.add_entity(event.entity)

    if event.entity.create_script is not None:
        event.entity.create_script()


def destroy_event_handler(event):
    event.entity = engine.game.Game.get_entity(event.entity)

    if event.entity is not None:
        if event.entity.destroy_script is not None:
            event.entity.destroy_script()

        engine.game.Game.remove_entity(event.entity)


def collision_event_handler(event):
    event.entity = engine.game.Game.get_entity(event.entity)
    event.other = engine.game.Game.get_entity(event.other)

    if event.entity is not None and event.other is not None:
        if event.entity.collision_script[event.other.name] is not None:
            event.entity.collision_script[event.other.name](event.other)


def step_event_handler(event):
    event.entity = engine.game.Game.get_entity(event.entity)

    if event.entity is not None:
        if event.entity.step_script is not None:
            event.entity.step_script()


def draw_event_handler(event):
    event.entity = engine.game.Game.get_entity(event.entity)

    if event.entity is not None:
        if event.entity.draw_script is not None:
            event.entity.draw_script()
        elif event.entity.visible:
            pass  # TODO: drawing


def input_event_handler(event):
    event.entity = engine.game.Game.get_entity(event.entity)

    if event.entity is not None:
        if event.input_type in event.entity.input_script:
            if isinstance(event.entity.input_script[event.input_type], dict):
                if event.entity.input_script[event.input_type][event.data] is not None:
                    event.entity.input_script[event.input_type][event.data]()
            else:
                if event.entity.input_script[event.input_type] is not None:
                    event.entity.input_script[event.input_type]()
