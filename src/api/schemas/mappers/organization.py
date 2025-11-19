from src.api.schemas.mappers.activity import activity_entity_to_schema
from src.api.schemas.mappers.building import building_entity_to_schema
from src.api.schemas.organization import OrganizationRead, PhoneNumberRead
from src.entity.organization import OrganizationEntity, PhoneNumberEntity


def phone_number_entity_to_schema(entity: PhoneNumberEntity) -> PhoneNumberRead:
    return PhoneNumberRead(id=entity.id, num=entity.num)


def organization_entity_to_schema(entity: OrganizationEntity) -> OrganizationRead:
    phone_numbers = [
        phone_number_entity_to_schema(phone_number)
        for phone_number in entity.phone_numbers
    ]
    building = building_entity_to_schema(entity.building)
    activities = [activity_entity_to_schema(activity) for activity in entity.activities]
    return OrganizationRead(
        id=entity.id,
        name=entity.name,
        phone_numbers=phone_numbers,
        building=building,
        activities=activities,
    )
