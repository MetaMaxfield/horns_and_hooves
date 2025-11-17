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


class Circle(BaseModel):
    lat: float = Field(
        ge=c.BUILDING_LATITUDE_MIN_VALUE, le=c.BUILDING_LATITUDE_MAX_VALUE
    )
    lon: float = Field(
        ge=c.BUILDING_LONGITUDE_MIN_VALUE, le=c.BUILDING_LONGITUDE_MAX_VALUE
    )
    radius: int = Field(ge=c.MIN_SEARCH_RADIUS, le=c.MAX_SEARCH_RADIUS)

    model_config = ConfigDict(extra="forbid", from_attributes=True)
