from src.entity.organization import OrganizationEntity
from src.usecase.protocols import IOrganizationRepo


class OrganizationUseCase:
    def __init__(self, repo: IOrganizationRepo):
        self.repo = repo

    async def get_org_by_recursive_activity(
        self, activity_name: str
    ) -> list[OrganizationEntity]:
        return self.repo.get_org_by_recursive_activity(activity_name)

    async def get_organizations_in_radius(
        self, lon: float, lat: float, radius: int
    ) -> list[OrganizationEntity]:
        return self.repo.get_organizations_in_radius(lon, lat, radius)

    async def get_organizations_in_rectangle(
        self, lon_min: float, lat_min: float, lon_max: float, lat_max: float
    ) -> list[OrganizationEntity]:
        return self.repo.get_organizations_in_rectangle(
            lon_min, lat_min, lon_max, lat_max
        )

    async def get_organizations_by_name(
        self, organization_name: str
    ) -> list[OrganizationEntity]:
        return self.repo.get_organizations_by_name(organization_name)

    async def get_organization_by_id(self, organization_id: int) -> OrganizationEntity:
        return self.repo.get_organization_by_id(organization_id)

    async def get_organizations_in_building(
        self, building_id: int
    ) -> list[OrganizationEntity]:
        return self.repo.get_organizations_in_building(building_id)

    async def get_organizations_with_activity(
        self, activity_id: int
    ) -> list[OrganizationEntity]:
        return self.repo.get_organizations_with_activity(activity_id)
