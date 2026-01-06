from fastapi import APIRouter

from .endpoints import health

router = APIRouter()
router.include_router(health.router, prefix="/health", tags=["health"])
