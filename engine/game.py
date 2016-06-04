from engine.entity import Entity, GUID, EntityModel


class Game:
    __entities = {}

    @classmethod
    def add_entity(cls, entity):
        if isinstance(entity, Entity):
            if entity.guid not in cls.__entities:
                cls.__entities[entity.guid] = entity
        elif isinstance(entity, EntityModel):
            pass

    @classmethod
    def remove_entity(cls, entity):
        if isinstance(entity, Entity):
            pass
        elif isinstance(entity, GUID):
            pass
