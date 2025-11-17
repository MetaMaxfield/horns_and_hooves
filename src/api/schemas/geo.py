from pydantic import BaseModel, ConfigDict, Field
from src.entity import constants as c


class Rectangle(BaseModel):
    lat_min: float = Field(
        ge=c.BUILDING_LATITUDE_MIN_VALUE, le=c.BUILDING_LATITUDE_MAX_VALUE
    )
    lat_max: float = Field(
        ge=c.BUILDING_LATITUDE_MIN_VALUE, le=c.BUILDING_LATITUDE_MAX_VALUE
    )
    lon_min: float = Field(
        ge=c.BUILDING_LONGITUDE_MIN_VALUE, le=c.BUILDING_LONGITUDE_MAX_VALUE
    )
    lon_max: float = Field(
        ge=c.BUILDING_LONGITUDE_MIN_VALUE, le=c.BUILDING_LONGITUDE_MAX_VALUE
    )

    model_config = ConfigDict(extra="forbid", from_attributes=True)
