import engine.events
import engine.game
import engine.spatial


def create_event_handler(event: engine.events.CreateEvent) -> None:
    if event.position is None:
        event.position = engine.spatial.Position()

    event.entity.position = event.position

    if event.entity.create_script is not None:
        event.entity.create_script(event.entity)


def destroy_event_handler(event: engine.events.DestroyEvent) -> None:
    event.entity = engine.game.Game.get_entity(event.entity)

    if event.entity is not None:
        if event.entity.destroy_script is not None:
            event.entity.destroy_script(event.entity)

        engine.game.Game.remove_entity(event.entity)


def collision_event_handler(event: engine.events.CollisionEvent) -> None:
    event.entity = engine.game.Game.get_entity(event.entity)
    event.other = engine.game.Game.get_entity(event.other)

    if event.entity is not None and event.other is not None:
        if event.entity.collision_script.get(event.other.name) is not None:
            event.entity.collision_script[event.other.name](event.entity, event.other)


def step_event_handler(event: engine.events.StepEvent) -> None:
    event.entity = engine.game.Game.get_entity(event.entity)

    if event.entity is not None:
        if event.entity.step_script is not None:
            event.entity.step_script(event.entity)

        event.entity.position.step()


def draw_event_handler(event: engine.events.DrawEvent) -> None:
    event.entity = engine.game.Game.get_entity(event.entity)

    if event.entity is not None:
        if event.entity.draw_script is not None:
            event.entity.draw_script(event.entity)
        elif event.entity.visible:
            if event.entity.sprite is not None:
                event.entity.sprite.x, event.entity.sprite.y = event.entity.position.x, event.entity.position.y
                event.entity.sprite.draw()


def input_event_handler(event: engine.events.InputEvent) -> None:
    event.entity = engine.game.Game.get_entity(event.entity)

    if event.entity is not None:
        if event.input_type in event.entity.input_script:
            if isinstance(event.entity.input_script[event.input_type], dict):
                if event.entity.input_script[event.input_type].get(event.data) is not None:
                    event.entity.input_script[event.input_type][event.data](event.entity)
            else:
                if event.entity.input_script.get(event.input_type) is not None:
                    event.entity.input_script[event.input_type](event.entity)
