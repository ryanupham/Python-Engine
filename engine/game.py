from engine.entity import Entity, GUID, EntityModel
from engine.events import EventManager, EventType, StepEvent, DrawEvent
import engine.event_handling as handlers
from engine.time import GlobalTimeline


class Game:
    __entities = {}
    steps_per_second = 60

    @classmethod
    def add_entity(cls, entity, position=None):
        if isinstance(entity, Entity):
            if entity.guid not in cls.__entities:
                if position is not None:
                    entity.position = position

                cls.__entities[entity.guid] = entity
        elif isinstance(entity, EntityModel):
            ent = Entity(model=entity, position=position)
            cls.__entities[ent.guid] = ent

    @classmethod
    def remove_entity(cls, entity):
        if isinstance(entity, Entity):
            del cls.__entities[entity.guid]
        elif isinstance(entity, GUID):
            del cls.__entities[entity]

    @classmethod
    def get_entity(cls, entity):
        if isinstance(entity, Entity):
            return cls.__entities.get(entity.guid)
        elif isinstance(entity, GUID):
            return cls.__entities.get(entity)

    @classmethod
    def get_entities(cls, model):
        if isinstance(model, EntityModel):
            name = model.name
        elif isinstance(model, str):
            name = model
        else:
            return []

        return [e for e in cls.__entities if e.name == name]

    @classmethod
    def initialize(cls):
        EventManager.register_handler(EventType.CREATE, handlers.create_event_handler)
        EventManager.register_handler(EventType.DESTROY, handlers.destroy_event_handler)
        EventManager.register_handler(EventType.COLLISION, handlers.collision_event_handler)
        EventManager.register_handler(EventType.STEP, handlers.step_event_handler)
        EventManager.register_handler(EventType.DRAW, handlers.draw_event_handler)
        EventManager.register_handler(EventType.INPUT, handlers.input_event_handler)

    @classmethod
    def main(cls):
        while not EventManager.empty():
            EventManager.handle_all()
            # detect collisions

        GlobalTimeline.step()

        for entity in cls.__entities.values():
            EventManager.raise_event(StepEvent(entity))

        while not EventManager.empty():
            EventManager.handle_all()
            # detect collisions

        EventManager.begin_draw()

        for entity in cls.__entities.values():
            EventManager.raise_event(DrawEvent(entity))

        EventManager.end_draw()

        # handle input
