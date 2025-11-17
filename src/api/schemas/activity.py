from pydantic import BaseModel, ConfigDict, Field

from src.entity.constants import ACTIVITY_NAME_MAX_LENGTH


class ActivityBase(BaseModel):
    name: str = Field(max_length=ACTIVITY_NAME_MAX_LENGTH)

    model_config = ConfigDict(extra="forbid", from_attributes=True)


class ActivityCreate(ActivityBase):
    pass


class ActivityRead(ActivityBase):
    id: int
