from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base
from src.entity.constants import ACTIVITY_NAME_MAX_LENGTH
from src.repo.types import IntPk

if TYPE_CHECKING:
    from src.repo.organization.models import Organization


class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[IntPk]
    name: Mapped[str] = mapped_column(String(ACTIVITY_NAME_MAX_LENGTH))
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("activities.id", ondelete="CASCADE")
    )

    organization: Mapped["Organization"] = relationship(
        secondary="organization_activities", back_populates="activities"
    )
    parent: Mapped["Activity"] = relationship(
        back_populates="childs", remote_side="Activity.id"
    )
    childs: Mapped["Activity"] = relationship(back_populates="parent")
