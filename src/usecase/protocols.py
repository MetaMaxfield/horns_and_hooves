from typing import Protocol

from src.entity.organization import OrganizationEntity


class IOrganizationRepo(Protocol):
    async def get_org_by_recursive_activity(
        self, activity_name: str
    ) -> list[OrganizationEntity]: ...

    async def get_organizations_in_radius(
        self, lon: float, lat: float, radius: int
    ) -> list[OrganizationEntity]: ...

    async def get_organizations_in_rectangle(
        self, lon_min: float, lat_min: float, lon_max: float, lat_max: float
    ) -> list[OrganizationEntity]: ...

    async def get_organizations_by_name(
        self, organization_name: str
    ) -> list[OrganizationEntity]: ...

    async def get_organization_by_id(
        self, organization_id: int
    ) -> OrganizationEntity: ...

    async def get_organizations_in_building(
        self, building_id: int
    ) -> list[OrganizationEntity]: ...

    async def get_organizations_with_activity(
        self, activity_id: int
    ) -> list[OrganizationEntity]: ...
