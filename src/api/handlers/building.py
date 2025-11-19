from fastapi import APIRouter, Depends

from src.api.dependencies import get_organization_use_case
from src.api.schemas.mappers.organization import organization_entity_to_schema
from src.api.schemas.organization import OrganizationRead
from src.usecase.organization import OrganizationUseCase


router = APIRouter(prefix="/buildings")


@router.get("/{building_id}/organizations", tags=["Организации"])
async def organizations_in_building(
    building_id: int, use_case: OrganizationUseCase = Depends(get_organization_use_case)
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
    orgs = await use_case.get_organizations_in_building(building_id)
    return [organization_entity_to_schema(org) for org in orgs]
