from src.entity.building import BuildingEntity
from src.entity.protocols import EntityMapper
from src.repo.building.models import Building


class BuildingMapper(EntityMapper[Building, BuildingEntity]):
    def to_entity(self, model: Building) -> BuildingEntity:
        return BuildingEntity(
            id=model.id,
            address=model.address,
            latitude=model.latitude,
            longitude=model.longitude,
        )
