from fastapi import APIRouter
from src.api.handlers.building import router as building_router


api_router = APIRouter(prefix="/api/v1")
api_router.include_router(building_router)
