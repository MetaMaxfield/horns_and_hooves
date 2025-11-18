from fastapi import Depends, HTTPException, Header, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.config import settings
from src.database import async_session_maker
from src.repo.organization.repo import OrganizationRepo
from src.usecase.organization import OrganizationUseCase


async def verify_api_key(x_api_key: str = Header(alias="X-API-Key")):
    if x_api_key != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API Key."
        )


async def get_db_session():
    async with async_session_maker() as session:
        yield session


async def get_organization_repo(session: AsyncSession = Depends(get_db_session)):
    return OrganizationRepo(session)


async def get_organization_use_case(
    org_repo: OrganizationRepo = Depends(get_organization_repo),
):
    return OrganizationUseCase(org_repo)
