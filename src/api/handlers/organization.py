from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import contains_eager, joinedload, selectinload
from geoalchemy2 import functions as geo_func

from src.api.dependencies import get_db_session
from src.api.schemas.geo import Rectangle
from src.api.schemas.organization import OrganizationRead
from src.repo.building.models import Building
from src.repo.organization.models import Organization


router = APIRouter(prefix="/organizations")


@router.get("/within-rectangle")
async def organizations_in_area(
    rectangle: Annotated[Rectangle, Query()],
    session: AsyncSession = Depends(get_db_session),
) -> list[OrganizationRead]:
    """Организации в области."""
    envelope = geo_func.ST_MakeEnvelope(
        rectangle.lon_min, rectangle.lat_min, rectangle.lon_max, rectangle.lat_max, 4326
    )
    query = (
        select(Organization)
        .join(Organization.building)
        .filter(geo_func.ST_Within(Building.geom, envelope))
        .options(contains_eager(Organization.building))
        .options(selectinload(Organization.phone_numbers))
        .options(selectinload(Organization.activities))
    )
    orgs = await session.execute(query)
    return orgs.scalars().all()


@router.get("/by-name")
async def organizations_by_name(
    organization_name: str, session: AsyncSession = Depends(get_db_session)
) -> list[OrganizationRead]:
    query = (
        select(Organization)
        .options(selectinload(Organization.phone_numbers))
        .options(selectinload(Organization.activities))
        .options(joinedload(Organization.building))
        .filter(Organization.name.ilike(f"%{organization_name}%"))
    )
    orgs = await session.execute(query)
    return orgs.scalars().all()


@router.get("/{organization_id}")
async def organization_by_id(
    organization_id: int, session: AsyncSession = Depends(get_db_session)
) -> OrganizationRead:
    query = (
        select(Organization)
        .filter_by(id=organization_id)
        .options(selectinload(Organization.phone_numbers))
        .options(selectinload(Organization.activities))
        .options(joinedload(Organization.building))
    )
    org = await session.scalar(query)
    if org:
        return org
    raise HTTPException(status_code=404)
