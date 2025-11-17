from typing import TYPE_CHECKING
from pydantic import BaseModel, ConfigDict, Field
from pydantic_extra_types.phone_numbers import PhoneNumber

from src.entity.constants import ORGANIZATION_NAME_MAX_LENGTH

if TYPE_CHECKING:
    from src.api.schemas.building import BuildingRead
    from src.api.schemas.activity import ActivityRead


class PhoneNumberBase(BaseModel):
    num: PhoneNumber

    model_config = ConfigDict(extra="forbid", from_attributes=True)


class PhoneNumberCreate(PhoneNumberBase):
    pass


class PhoneNumberRead(PhoneNumberBase):
    id: int


class OrganizationBase(BaseModel):
    name: str = Field(max_length=ORGANIZATION_NAME_MAX_LENGTH)

    model_config = ConfigDict(extra="forbid", from_attributes=True)


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationRead(OrganizationBase):
    id: int

    phone_numbers: list["PhoneNumberRead"]
    building: "BuildingRead"
    activities: "ActivityRead"
