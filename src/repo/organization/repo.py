from sqlalchemy import cast, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import contains_eager, joinedload, selectinload
from src.entity.mappers.organization import OrganizationMapper
from src.entity.organization import OrganizationEntity
from src.repo.activity.models import Activity
from src.repo.associations.models import OrganizationActivity
from src.repo.building.models import Building
from src.repo.organization.models import Organization
from geoalchemy2 import Geography, functions as geo_func


class OrganizationRepo:
    def __init__(self, session: AsyncSession):
        self.session = session
        self._mapper = OrganizationMapper()

    async def get_org_by_recursive_activity(
        self, activity_name: str
    ) -> list[OrganizationEntity]:
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

        result = await self.session.execute(query)
        orgs = result.scalars().all()
        return [self._mapper.to_entity(org) for org in orgs] if orgs else []

    async def get_organizations_in_radius(
        self, lon: float, lat: float, radius: int
    ) -> list[OrganizationEntity]:
        center_point = geo_func.ST_SetSRID(geo_func.ST_MakePoint(lon, lat), 4326)
        query = (
            select(Organization)
            .join(Organization.building)
            .filter(
                geo_func.ST_DWithin(
                    cast(Building.geom, Geography),
                    cast(center_point, Geography),
                    radius,
                )
            )
            .options(contains_eager(Organization.building))
            .options(selectinload(Organization.phone_numbers))
            .options(selectinload(Organization.activities))
        )
        result = await self.session.execute(query)
        orgs = result.scalars().all()
        return [self._mapper.to_entity(org) for org in orgs] if orgs else []

    async def get_organizations_in_rectangle(
        self, lon_min: float, lat_min: float, lon_max: float, lat_max: float
    ) -> list[OrganizationEntity]:
        envelope = geo_func.ST_MakeEnvelope(lon_min, lat_min, lon_max, lat_max, 4326)
        query = (
            select(Organization)
            .join(Organization.building)
            .filter(geo_func.ST_Within(Building.geom, envelope))
            .options(contains_eager(Organization.building))
            .options(selectinload(Organization.phone_numbers))
            .options(selectinload(Organization.activities))
        )
        result = await self.session.execute(query)
        orgs = result.scalars().all()
        return [self._mapper.to_entity(org) for org in orgs] if orgs else []

    async def get_organizations_by_name(
        self, organization_name: str
    ) -> list[OrganizationEntity]:
        query = (
            select(Organization)
            .options(selectinload(Organization.phone_numbers))
            .options(selectinload(Organization.activities))
            .options(joinedload(Organization.building))
            .filter(Organization.name.ilike(f"%{organization_name}%"))
        )
        result = await self.session.execute(query)
        orgs = result.scalars().all()
        return [self._mapper.to_entity(org) for org in orgs] if orgs else []

    async def get_organization_by_id(self, organization_id: int) -> OrganizationEntity:
        query = (
            select(Organization)
            .filter_by(id=organization_id)
            .options(selectinload(Organization.phone_numbers))
            .options(selectinload(Organization.activities))
            .options(joinedload(Organization.building))
        )
        org = await self.session.scalar(query)
        return self._mapper.to_entity(org) if org else None

    async def get_organizations_in_building(
        self, building_id: int
    ) -> list[OrganizationEntity]:
        query = (
            select(Organization)
            .filter_by(building_id=building_id)
            .options(selectinload(Organization.phone_numbers))
            .options(selectinload(Organization.activities))
            .options(joinedload(Organization.building))
        )
        result = await self.session.execute(query)
        orgs = result.scalars().all()
        return [self._mapper.to_entity(org) for org in orgs] if orgs else []

    async def get_organizations_with_activity(
        self, activity_id: int
    ) -> list[OrganizationEntity]:
        query = (
            select(Organization)
            .filter(Organization.activities.any(Activity.id == activity_id))
            .options(selectinload(Organization.phone_numbers))
            .options(selectinload(Organization.activities))
            .options(joinedload(Organization.building))
        )
        result = await self.session.execute(query)
        orgs = result.scalars().all()
        return [self._mapper.to_entity(org) for org in orgs] if orgs else []
