from engine.entity import Entity, GUID, EntityModel


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
