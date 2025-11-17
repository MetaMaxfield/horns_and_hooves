from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from src.api.dependencies import get_db_session
from src.api.schemas.organization import OrganizationRead
from src.repo.organization.models import Organization


router = APIRouter(prefix="/buildings")


@router.get("/{building_id}/organizations", tags=["Организации"])
async def organizations_in_building(
    building_id: int, session: AsyncSession = Depends(get_db_session)
) -> list[OrganizationRead]:
    """
    Handler поиска организаций по ID здания.\n
    \n
    Query params:\n
        building_id (int): ID здания, по которому производится поиск организаций.\n
    \n
    Returns:\n
        list[OrganizationRead]: Список найденных организаций с подгруженными
        контактами и информацией о здании.\n
    """
    query = (
        select(Organization)
        .filter_by(building_id=building_id)
        .options(selectinload(Organization.phone_numbers))
        .options(selectinload(Organization.activities))
        .options(joinedload(Organization.building))
    )
    result = await session.execute(query)
    return result.scalars().all()
