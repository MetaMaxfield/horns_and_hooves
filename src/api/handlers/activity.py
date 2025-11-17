from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from src.api.dependencies import get_db_session
from src.api.schemas.organization import OrganizationRead
from src.repo.activity.models import Activity
from src.repo.organization.models import Organization


router = APIRouter(prefix="/activities")


@router.get("/{activity_id}/organizations")
async def organizations_with_activity(
    activity_id: int, session: AsyncSession = Depends(get_db_session)
) -> list[OrganizationRead]:
    query = (
        select(Organization)
        .filter(Organization.activities.any(Activity.id == activity_id))
        .options(selectinload(Organization.phone_numbers))
        .options(selectinload(Organization.activities))
        .options(joinedload(Organization.building))
    )
    result = await session.execute(query)
    return result.scalars().all()
