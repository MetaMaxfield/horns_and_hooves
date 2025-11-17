from fastapi import APIRouter
from src.api.handlers.building import router as building_router
from src.api.handlers.activity import router as activity_router


api_router = APIRouter(prefix="/api/v1")
api_router.include_router(building_router)
api_router.include_router(activity_router)
