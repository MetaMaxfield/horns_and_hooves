from fastapi import APIRouter, Depends

from src.api.dependencies import get_organization_use_case
from src.api.schemas.mappers.organization import organization_entity_to_schema
from src.api.schemas.organization import OrganizationRead
from src.usecase.organization import OrganizationUseCase


router = APIRouter(prefix="/activities")


@router.get("/{activity_id}/organizations", tags=["Организации"])
async def organizations_with_activity(
    activity_id: int, use_case: OrganizationUseCase = Depends(get_organization_use_case)
) -> list[OrganizationRead]:
    """
    Handler поиска организаций по ID вида деятельности.\n
    \n
    Query params:\n
        activity_id (int): ID вида деятельности.\n
    \n
    Returns:\n
        list[OrganizationRead]: Список организаций с подгруженными связями.\n
    """
    orgs = await use_case.get_organizations_with_activity(activity_id)
    return [organization_entity_to_schema(org) for org in orgs]
