from sqlalchemy.orm import Session

from ..models import ClaimStatus, ExperienceClaim, VerificationOutcome, VerificationRecord
from ..schemas.models import VerificationDecision


def create_verification(db: Session, claim: ExperienceClaim, verifier_id: str, decision: VerificationDecision, organization_id: str | None = None) -> VerificationRecord:
    record = VerificationRecord(
        claim_id=claim.id,
        verifier_id=verifier_id,
        organization_id=organization_id,
        outcome=decision.outcome,
        notes=decision.notes,
        role_type=decision.role_type,
        verified_start_date=decision.verified_start_date,
        verified_end_date=decision.verified_end_date,
        valid_until=decision.valid_until,
    )
    db.add(record)

    claim.status = ClaimStatus.verified if decision.outcome == VerificationOutcome.approved else ClaimStatus.rejected
    db.add(claim)

    db.commit()
    db.refresh(record)
    db.refresh(claim)
    return record


def get_for_claim(db: Session, claim_id: str) -> list[VerificationRecord]:
    return db.query(VerificationRecord).filter(VerificationRecord.claim_id == claim_id).all()


def inbox_for_verifier(db: Session, verifier_id: str) -> list[ExperienceClaim]:
    # Simplified: all pending claims for now; org linkage can refine later
    return db.query(ExperienceClaim).filter(ExperienceClaim.status == ClaimStatus.pending).all()
