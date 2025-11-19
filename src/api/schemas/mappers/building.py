from src.api.schemas.building import BuildingRead
from src.entity.building import BuildingEntity


def building_entity_to_schema(entity: BuildingEntity) -> BuildingRead:
    return BuildingRead(
        id=entity.id,
        address=entity.address,
        latitude=entity.latitude,
        longitude=entity.longitude,
    )
