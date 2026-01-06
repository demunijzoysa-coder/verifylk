from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ....db import get_db
from ....models import ClaimStatus
from ....repositories.claims import get_claim
from ....schemas.models import ExperienceClaimOut

router = APIRouter()


@router.get("/{token}", response_model=ExperienceClaimOut, summary="Public verification report")
def view_report(token: str, db: Session = Depends(get_db)):
    # MVP stub: token equals claim_id; replace with signed token validation
    claim = get_claim(db, token)
    if not claim or claim.status != ClaimStatus.verified:
        raise HTTPException(status_code=404, detail="Report not found or not verified")
    return claim
