from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ....dependencies import require_role
from ....db import get_db
from ....models import Dispute, DisputeStatus, Organization, OrgStatus, User, UserRole

router = APIRouter()


@router.get("/orgs", response_model=list[dict], summary="List organizations for verification")
def list_orgs(current_user: User = Depends(require_role(UserRole.admin)), db: Session = Depends(get_db)):
    orgs = db.query(Organization).all()
    return [{"id": o.id, "name": o.name, "status": o.verified_status.value, "contact_email": o.contact_email} for o in orgs]


@router.post("/orgs/{org_id}/verify", summary="Update organization verification status")
def verify_org(
    org_id: str,
    status_value: OrgStatus = OrgStatus.verified,
    current_user: User = Depends(require_role(UserRole.admin)),
    db: Session = Depends(get_db),
):
    org = db.query(Organization).filter(Organization.id == org_id).first()
    if not org:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
    org.verified_status = status_value
    db.add(org)
    db.commit()
    db.refresh(org)
    return {"id": org.id, "status": org.verified_status.value}


@router.get("/disputes", response_model=list[dict], summary="List disputes")
def list_disputes(current_user: User = Depends(require_role(UserRole.admin)), db: Session = Depends(get_db)):
    disputes = db.query(Dispute).all()
    return [
        {
            "id": d.id,
            "claim_id": d.claim_id,
            "status": d.status.value,
            "reason": d.reason,
            "resolution_notes": d.resolution_notes,
        }
        for d in disputes
    ]


@router.post("/disputes/{dispute_id}/decision", summary="Resolve or dismiss dispute")
def decide_dispute(
    dispute_id: str,
    status_value: DisputeStatus,
    notes: str | None = None,
    current_user: User = Depends(require_role(UserRole.admin)),
    db: Session = Depends(get_db),
):
    dispute = db.query(Dispute).filter(Dispute.id == dispute_id).first()
    if not dispute:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dispute not found")
    dispute.status = status_value
    dispute.resolution_notes = notes
    db.add(dispute)
    db.commit()
    db.refresh(dispute)
    return {"id": dispute.id, "status": dispute.status.value, "resolution_notes": dispute.resolution_notes}


@router.get("/audit", response_model=list[dict], summary="List audit log entries (recent)")
def list_audit(current_user: User = Depends(require_role(UserRole.admin)), db: Session = Depends(get_db)):
    from ....models import AuditLog

    logs = db.query(AuditLog).order_by(AuditLog.created_at.desc()).limit(50).all()
    return [
        {
            "id": log.id,
            "action": log.action,
            "actor_id": log.actor_id,
            "entity_type": log.entity_type,
            "entity_id": log.entity_id,
            "metadata": log.details,
            "created_at": log.created_at,
        }
        for log in logs
    ]
