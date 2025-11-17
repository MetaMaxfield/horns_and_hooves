from fastapi import APIRouter, Depends
from src.api.dependencies import verify_api_key
from src.api.handlers.building import router as building_router
from src.api.handlers.activity import router as activity_router
from src.api.handlers.organization import router as organization_router


api_router = APIRouter(prefix="/api/v1", dependencies=[Depends(verify_api_key)])
api_router.include_router(building_router)
api_router.include_router(activity_router)
api_router.include_router(organization_router)
