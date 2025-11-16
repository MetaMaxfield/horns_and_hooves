from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base
from src.entity.constants import (
    ORGANIZATION_NAME_MAX_LENGTH,
    PHONENUMBER_NUM_MAX_LENGTH,
)
from src.repo.types import IntPk

if TYPE_CHECKING:
    from src.repo.building.models import Building
    from src.repo.activity.models import Activity


class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[IntPk]
    name: Mapped[str] = mapped_column(String(ORGANIZATION_NAME_MAX_LENGTH))
    building_id: Mapped[int] = mapped_column(
        ForeignKey("buildings.id", ondelete="CASCADE")
    )

    phone_numbers: Mapped[list["PhoneNumber"]] = relationship(
        back_populates="organization"
    )
    building: Mapped["Building"] = relationship(back_populates="organization")
    activities: Mapped[list["Activity"]] = relationship(
        secondary="organization_activities", back_populates="organization"
    )


class PhoneNumber(Base):
    __tablename__ = "phone_numbers"

    id: Mapped[IntPk]
    num: Mapped[str] = mapped_column(String(PHONENUMBER_NUM_MAX_LENGTH))
    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE")
    )

    organization: Mapped["Organization"] = relationship(back_populates="phone_numbers")
