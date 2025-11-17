from fastapi import HTTPException, Header, status
from src.config import settings
from src.database import async_session_maker


async def verify_api_key(x_api_key: str = Header(alias="X-API-Key")):
    if x_api_key != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API Key."
        )


async def get_db_session():
    async with async_session_maker() as session:
        yield session
