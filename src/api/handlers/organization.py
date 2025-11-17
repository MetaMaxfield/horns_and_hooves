from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import cast, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import contains_eager, joinedload, selectinload
from geoalchemy2 import Geography, functions as geo_func

from src.api.dependencies import get_db_session
from src.api.schemas.geo import Circle, Rectangle
from src.api.schemas.organization import OrganizationRead
from src.repo.activity.models import Activity
from src.repo.associations.models import OrganizationActivity
from src.repo.building.models import Building
from src.repo.organization.models import Organization


router = APIRouter(prefix="/organizations")


@router.get("/recursive-search-by-activity", tags=["Организации"])
async def organizations_by_recursive_activity(
    activity_name: str, session: AsyncSession = Depends(get_db_session)
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
    # базовая часть CTE — сам activity
    subtree = (
        select(Activity.id)
        .filter(Activity.name.ilike(f"%{activity_name}%"))
        .cte(name="subtree", recursive=True)
    )

    # рекурсивная часть — берем те activity, у которых parent_id == id из subtree
    subtree = subtree.union_all(
        select(Activity.id).where(Activity.parent_id == subtree.c.id)
    )

    # теперь выбираем организации, у которых есть activity из subtree
    query = (
        select(Organization)
        .join(
            OrganizationActivity,
            Organization.id == OrganizationActivity.organization_id,
        )
        .join(subtree, OrganizationActivity.activity_id == subtree.c.id)
        .options(
            selectinload(Organization.phone_numbers),
            selectinload(Organization.activities),
            joinedload(Organization.building),
        )
        .distinct()
    )

    orgs = await session.execute(query)
    return orgs.scalars().all()


@router.get("/within-radius", tags=["Организации"])
async def organizations_in_radius(
    circle: Annotated[Circle, Query()],
    session: AsyncSession = Depends(get_db_session),
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
    center_point = geo_func.ST_SetSRID(
        geo_func.ST_MakePoint(circle.lon, circle.lat), 4326
    )
    query = (
        select(Organization)
        .join(Organization.building)
        .filter(
            geo_func.ST_DWithin(
                cast(Building.geom, Geography),
                cast(center_point, Geography),
                circle.radius,
            )
        )
        .options(contains_eager(Organization.building))
        .options(selectinload(Organization.phone_numbers))
        .options(selectinload(Organization.activities))
    )
    orgs = await session.execute(query)
    return orgs.scalars().all()


@router.get("/within-rectangle", tags=["Организации"])
async def organizations_in_rectangle(
    rectangle: Annotated[Rectangle, Query()],
    session: AsyncSession = Depends(get_db_session),
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


@router.get("/by-name", tags=["Организации"])
async def organizations_by_name(
    organization_name: str, session: AsyncSession = Depends(get_db_session)
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
    query = (
        select(Organization)
        .options(selectinload(Organization.phone_numbers))
        .options(selectinload(Organization.activities))
        .options(joinedload(Organization.building))
        .filter(Organization.name.ilike(f"%{organization_name}%"))
    )
    orgs = await session.execute(query)
    return orgs.scalars().all()


@router.get("/{organization_id}", tags=["Организации"])
async def organization_by_id(
    organization_id: int, session: AsyncSession = Depends(get_db_session)
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
