from src.entity.protocols import EntityMapper
from src.entity.activity import ActivityEntity
from src.repo.activity.models import Activity


class ActivityMapper(EntityMapper[Activity, ActivityEntity]):
    def to_entity(self, model: Activity) -> ActivityEntity:
        return ActivityEntity(id=model.id, name=model.name)
