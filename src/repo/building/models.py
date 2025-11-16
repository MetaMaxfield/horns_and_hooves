from typing import TYPE_CHECKING, Any
from sqlalchemy import CheckConstraint, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base
from src.entity.constants import BUILDING_ADDRESS_MAX_LENGTH
from src.repo.types import IntPk
from src.entity import constants as c
from geoalchemy2 import Geometry

if TYPE_CHECKING:
    from src.repo.organization.models import Organization


class Building(Base):
    __tablename__ = "buildings"

    id: Mapped[IntPk]
    address: Mapped[str] = mapped_column(String(BUILDING_ADDRESS_MAX_LENGTH))
    latitude: Mapped[float]
    longitude: Mapped[float]
    geom: Mapped[Any] = mapped_column(Geometry(geometry_type="POINT", srid=4326))

    organizations: Mapped[list["Organization"]] = relationship(
        back_populates="building"
    )

    __table_args__ = (
        CheckConstraint(
            f"latitude >= {c.BUILDING_LATITUDE_MIN_VALUE} AND latitude <= {c.BUILDING_LATITUDE_MAX_VALUE}",
            name="latitude_range",
        ),
        CheckConstraint(
            f"longitude >= {c.BUILDING_LONGITUDE_MIN_VALUE} AND longitude <= {c.BUILDING_LONGITUDE_MAX_VALUE}",
            name="longitude_range",
        ),
    )
