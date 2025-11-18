from src.entity.mappers.activity import ActivityMapper
from src.entity.mappers.building import BuildingMapper
from src.entity.organization import OrganizationEntity, PhoneNumberEntity
from src.entity.protocols import EntityMapper
from src.repo.organization.models import Organization, PhoneNumber


class PhoneNumberMapper(EntityMapper[PhoneNumber, PhoneNumberEntity]):
    def to_entity(self, model: PhoneNumber) -> PhoneNumberEntity:
        return PhoneNumberEntity(id=model.id, num=model.num)


class OrganizationMapper(EntityMapper[Organization, OrganizationEntity]):
    def __init__(self):
        self._building_mapper = BuildingMapper()
        self._activity_mapper = ActivityMapper()
        self._phone_number_mapper = PhoneNumberMapper()

    def to_entity(self, model: Organization) -> OrganizationEntity:
        building = self._building_mapper.to_entity(model.building)
        activities = [
            self._activity_mapper.to_entity(activity) for activity in model.activities
        ]
        phone_numbers = [
            self._phone_number_mapper.to_entity(phone_number)
            for phone_number in model.phone_numbers
        ]
        return OrganizationEntity(
            id=model.id,
            name=model.name,
            building=building,
            activities=activities,
            phone_numbers=phone_numbers,
        )
