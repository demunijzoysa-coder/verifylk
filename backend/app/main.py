from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.routes import router as api_router
from .config import get_settings
from .db import Base, engine
from .db import SessionLocal
from .middleware.audit import audit_middleware
from .repositories.users import get_by_email, create_user
from .models import Organization, OrgStatus, UserRole


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.project_name)
    Base.metadata.create_all(bind=engine)

    def seed_admin():
        db = SessionLocal()
        try:
            admin_email = "admin@gmail.com"
            existing = get_by_email(db, admin_email)
            if not existing:
                create_user(
                    db=db,
                    email=admin_email,
                    password="1234",
                    full_name="Admin",
                    role=UserRole.admin,
                    org_id=None,
                )
        finally:
            db.close()

    def seed_orgs():
        db = SessionLocal()
        try:
            existing = db.query(Organization).count()
            if existing == 0:
                samples = [
                    Organization(name="Community Bridge", verified_status=OrgStatus.pending, contact_email="org@community.lk"),
                    Organization(name="TechWorks Jaffna", verified_status=OrgStatus.verified, contact_email="hello@techworks.lk"),
                    Organization(name="GreenHands", verified_status=OrgStatus.pending, contact_email="team@greenhands.lk"),
                ]
                db.add_all(samples)
                db.commit()
        finally:
            db.close()

    seed_admin()
    seed_orgs()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.middleware("http")(audit_middleware)

    @app.get("/", summary="Root")
    def root():
        return {"message": "VerifyLK API", "environment": settings.environment}

    app.include_router(api_router, prefix="/api")
    return app


app = create_app()
