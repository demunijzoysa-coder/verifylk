from fastapi import APIRouter

from .endpoints import auth, claims, health, reports, verifications

router = APIRouter()
router.include_router(health.router, prefix="/health", tags=["health"])
router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(claims.router, prefix="/claims", tags=["claims"])
router.include_router(verifications.router, prefix="/verifications", tags=["verifications"])
router.include_router(reports.router, prefix="/reports", tags=["reports"])
