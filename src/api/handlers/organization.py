from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query

from src.api.dependencies import get_organization_use_case
from src.api.schemas.geo import Circle, Rectangle
from src.api.schemas.mappers.organization import organization_entity_to_schema
from src.api.schemas.organization import OrganizationRead
from src.usecase.organization import OrganizationUseCase


router = APIRouter(prefix="/organizations")


@router.get("/recursive-search-by-activity", tags=["Организации"])
async def organizations_by_recursive_activity(
    activity_name: str,
    use_case: OrganizationUseCase = Depends(get_organization_use_case),
) -> list[OrganizationRead]:
    """
    Handler поиска организаций по названию вида деятельности с рекурсивным обходом дерева.\n
    \n
    Query params:\n
        activity_name (str): Название вида деятельности для поиска.\n
    \n
    Returns:\n
        list[OrganizationRead]: Список организаций, связанных с найденными видами деятельности.\n
    """
    orgs = await use_case.get_org_by_recursive_activity(activity_name)
    return [organization_entity_to_schema(org) for org in orgs]


@router.get("/within-radius", tags=["Организации"])
async def organizations_in_radius(
    circle: Annotated[Circle, Query()],
    use_case: OrganizationUseCase = Depends(get_organization_use_case),
) -> list[OrganizationRead]:
    """
    Handler поиска организаций в радиусе от указанной точки.\n
    \n
    Query params:\n
        lat (float): Широта центра круга.\n
        lon (float): Долгота центра круга.\n
        radius (int): Радиус поиска в метрах.\n
    \n
    Returns:\n
        list[OrganizationRead]: Список организаций, находящихся в указанном радиусе.\n
    """
    orgs = await use_case.get_organizations_in_radius(
        circle.lon, circle.lat, circle.radius
    )
    return [organization_entity_to_schema(org) for org in orgs]


@router.get("/within-rectangle", tags=["Организации"])
async def organizations_in_rectangle(
    rectangle: Annotated[Rectangle, Query()],
    use_case: OrganizationUseCase = Depends(get_organization_use_case),
) -> list[OrganizationRead]:
    """
    Handler поиска организаций в прямоугольной области.\n
    \n
    Query params:\n
        lat_min (float): Минимальная широта прямоугольника.\n
        lat_max (float): Максимальная широта прямоугольника.\n
        lon_min (float): Минимальная долгота прямоугольника.\n
        lon_max (float): Максимальная долгота прямоугольника.\n
    \n
    Returns:\n
        list[OrganizationRead]: Список организаций, находящихся в указанной области.\n
    """
    orgs = await use_case.get_organizations_in_rectangle(
        rectangle.lon_min, rectangle.lat_min, rectangle.lon_max, rectangle.lat_max
    )
    return [organization_entity_to_schema(org) for org in orgs]


@router.get("/by-name", tags=["Организации"])
async def organizations_by_name(
    organization_name: str,
    use_case: OrganizationUseCase = Depends(get_organization_use_case),
) -> list[OrganizationRead]:
    """
    Handler поиска организаций по названию.\n
    \n
    Query params:\n
        organization_name (str): Подстрока для поиска в названии организации.\n
    \n
    Returns:\n
        list[OrganizationRead]: Список организаций, название которых совпадает с поиском.\n
    """
    orgs = await use_case.get_organizations_by_name(organization_name)
    return [organization_entity_to_schema(org) for org in orgs]


@router.get("/{organization_id}", tags=["Организации"])
async def organization_by_id(
    organization_id: int,
    use_case: OrganizationUseCase = Depends(get_organization_use_case),
) -> OrganizationRead:
    """
    Handler получения информации об организации по её ID.\n
    \n
    Query params:\n
        organization_id (int): ID организации для поиска.\n
    \n
    Returns:\n
        OrganizationRead: Информация об организации.\n
    """
    org = await use_case.get_organization_by_id(organization_id)
    if not org:
        raise HTTPException(status_code=404)
    return organization_entity_to_schema(org)
