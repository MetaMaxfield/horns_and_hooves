from dataclasses import dataclass

from src.entity.activity import ActivityEntity
from src.entity.building import BuildingEntity


@dataclass(slots=True)
class PhoneNumberEntity:
    id: int
    num: str


@dataclass(slots=True)
class OrganizationEntity:
    id: int
    name: str
    building: BuildingEntity
    activities: list[ActivityEntity]
    phone_numbers: list[PhoneNumberEntity]
