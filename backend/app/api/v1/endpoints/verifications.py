from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ....dependencies import require_role
from ....db import get_db
from ....models import ExperienceClaim, User, UserRole
from ....repositories.claims import get_claim
from ....repositories.verifications import create_verification, get_for_claim, inbox_for_verifier
from ....schemas.models import ExperienceClaimOut, VerificationDecision, VerificationRecordOut
from ....services.scoring import calculate_score

router = APIRouter()


@router.get("/inbox", response_model=list[ExperienceClaimOut], summary="Pending claims to verify")
def list_inbox(current_user: User = Depends(require_role(UserRole.verifier)), db: Session = Depends(get_db)):
    return inbox_for_verifier(db, current_user.id)


@router.post("/{claim_id}/decision", response_model=VerificationRecordOut, summary="Approve or reject a claim")
def decide(
    claim_id: str,
    decision: VerificationDecision,
    current_user: User = Depends(require_role(UserRole.verifier)),
    db: Session = Depends(get_db),
):
    claim = get_claim(db, claim_id)
    if not claim:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Claim not found")

    record = create_verification(db, claim, verifier_id=current_user.id, decision=decision)

    verifications = get_for_claim(db, claim.id)
    score, breakdown = calculate_score(claim, verifications)
    claim.credibility_score = score
    claim.credibility_breakdown = [b.model_dump() for b in breakdown]
    db.add(claim)
    db.commit()
    db.refresh(record)
    return record
