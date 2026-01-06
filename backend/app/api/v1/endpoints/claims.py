from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ....dependencies import get_current_user, require_role
from ....db import get_db
from ....models import ClaimStatus, ExperienceClaim, User, UserRole
from ....repositories.claims import create_claim, get_claim, get_claims_for_candidate, update_claim
from ....schemas.models import ExperienceClaimCreate, ExperienceClaimOut, ExperienceClaimUpdate

router = APIRouter()


@router.get("", response_model=list[ExperienceClaimOut], summary="List my claims")
def list_claims(
    current_user: User = Depends(require_role(UserRole.candidate)), db: Session = Depends(get_db)
):
    return get_claims_for_candidate(db, current_user.id)


@router.post("", response_model=ExperienceClaimOut, status_code=status.HTTP_201_CREATED, summary="Create claim")
def create_new_claim(
    payload: ExperienceClaimCreate,
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    return create_claim(db, current_user.id, payload)


def _ensure_owner(claim: ExperienceClaim, user: User):
    if claim.candidate_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your claim")


@router.get("/{claim_id}", response_model=ExperienceClaimOut, summary="Get claim by id")
def get_claim_by_id(
    claim_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    claim = get_claim(db, claim_id)
    if not claim:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Claim not found")
    if current_user.role != UserRole.admin:
        _ensure_owner(claim, current_user)
    return claim


@router.put("/{claim_id}", response_model=ExperienceClaimOut, summary="Update claim (draft/pending)")
def update_claim_by_id(
    claim_id: str,
    payload: ExperienceClaimUpdate,
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    claim = get_claim(db, claim_id)
    if not claim:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Claim not found")
    _ensure_owner(claim, current_user)
    if claim.status not in [ClaimStatus.draft, ClaimStatus.pending]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only draft/pending claims can be edited")
    return update_claim(db, claim, payload)


@router.post("/{claim_id}/request-verification", response_model=ExperienceClaimOut, summary="Request verification")
def request_verification(
    claim_id: str,
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    claim = get_claim(db, claim_id)
    if not claim:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Claim not found")
    _ensure_owner(claim, current_user)
    claim.status = ClaimStatus.pending
    db.add(claim)
    db.commit()
    db.refresh(claim)
    # Email dispatch stub lives in services; wired later
    return claim
