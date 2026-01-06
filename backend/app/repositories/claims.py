from sqlalchemy.orm import Session

from ..models import ClaimStatus, ExperienceClaim
from ..schemas.models import ExperienceClaimCreate, ExperienceClaimUpdate


def create_claim(db: Session, candidate_id: str, payload: ExperienceClaimCreate) -> ExperienceClaim:
    claim = ExperienceClaim(
        candidate_id=candidate_id,
        title=payload.title,
        claim_type=payload.claim_type,
        organization_name=payload.organization_name,
        supervisor_name=payload.supervisor_name,
        supervisor_contact=payload.supervisor_contact,
        start_date=payload.start_date,
        end_date=payload.end_date,
        description=payload.description,
        skill_tags=payload.skill_tags or [],
        evidence_visibility=payload.evidence_visibility,
        status=ClaimStatus.draft,
    )
    db.add(claim)
    db.commit()
    db.refresh(claim)
    return claim


def get_claims_for_candidate(db: Session, candidate_id: str) -> list[ExperienceClaim]:
    return db.query(ExperienceClaim).filter(ExperienceClaim.candidate_id == candidate_id).all()


def get_claim(db: Session, claim_id: str) -> ExperienceClaim | None:
    return db.query(ExperienceClaim).filter(ExperienceClaim.id == claim_id).first()


def update_claim(db: Session, claim: ExperienceClaim, payload: ExperienceClaimUpdate) -> ExperienceClaim:
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(claim, field, value)
    db.commit()
    db.refresh(claim)
    return claim
