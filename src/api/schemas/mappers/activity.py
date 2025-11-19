from src.api.schemas.activity import ActivityRead
from src.entity.activity import ActivityEntity


def activity_entity_to_schema(entity: ActivityEntity) -> ActivityRead:
    return ActivityRead(id=entity.id, name=entity.name)
