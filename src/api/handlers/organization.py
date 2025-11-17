from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from src.api.dependencies import get_db_session
from src.api.schemas.organization import OrganizationRead
from src.repo.organization.models import Organization


router = APIRouter(prefix="/organizations")


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
