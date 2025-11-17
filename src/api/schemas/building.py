from pydantic import BaseModel, ConfigDict, Field

from src.entity import constants as c


class BuildingBase(BaseModel):
    address: str = Field(max_length=c.BUILDING_ADDRESS_MAX_LENGTH)
    latitude: float = Field(
        ge=c.BUILDING_LATITUDE_MIN_VALUE, le=c.BUILDING_LATITUDE_MAX_VALUE
    )
    longitude: float = Field(
        ge=c.BUILDING_LONGITUDE_MIN_VALUE, le=c.BUILDING_LONGITUDE_MAX_VALUE
    )

    model_config = ConfigDict(extra="forbid", from_attributes=True)


class BuildingCreate(BuildingBase):
    pass


class BuildingRead(BuildingBase):
    id: int
