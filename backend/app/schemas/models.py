from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field

from ..models import (
    ClaimStatus,
    DisputeStatus,
    EvidenceVisibility,
    UserRole,
    VerificationOutcome,
)


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str | None = None
    role: UserRole | None = None
    exp: int | None = None


class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: UserRole

    class Config:
        use_enum_values = True


class UserCreate(UserBase):
    password: str
    organization_name: str | None = None


class UserOut(UserBase):
    id: str

    class Config:
        from_attributes = True


class EvidenceFileOut(BaseModel):
    id: str
    file_name: str
    mime_type: str
    is_public: bool
    created_at: datetime

    class Config:
        from_attributes = True


class ClaimBase(BaseModel):
    title: str
    claim_type: str
    organization_name: str
    supervisor_name: str
    supervisor_contact: str
    start_date: date
    end_date: date
    description: str
    skill_tags: List[str] | None = None
    evidence_visibility: EvidenceVisibility = EvidenceVisibility.verifier_only

    class Config:
        use_enum_values = True


class ExperienceClaimCreate(ClaimBase):
    pass


class ExperienceClaimUpdate(BaseModel):
    title: Optional[str] = None
    claim_type: Optional[str] = None
    organization_name: Optional[str] = None
    supervisor_name: Optional[str] = None
    supervisor_contact: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    description: Optional[str] = None
    skill_tags: Optional[List[str]] = None
    evidence_visibility: Optional[EvidenceVisibility] = None


class ScoreBreakdown(BaseModel):
    factor: str
    score: float
    reason: str


class ExperienceClaimOut(ClaimBase):
    id: str
    status: ClaimStatus
    credibility_score: float | None = None
    credibility_breakdown: List[ScoreBreakdown] | None = None
    created_at: datetime
    updated_at: datetime
    evidence: List[EvidenceFileOut] | None = None

    class Config:
        from_attributes = True


class VerificationDecision(BaseModel):
    outcome: VerificationOutcome
    notes: str | None = None
    role_type: str | None = None
    verified_start_date: date | None = None
    verified_end_date: date | None = None
    valid_until: date | None = None

    class Config:
        use_enum_values = True


class VerificationRecordOut(BaseModel):
    id: str
    outcome: VerificationOutcome
    notes: str | None = None
    role_type: str | None = None
    verified_start_date: date | None = None
    verified_end_date: date | None = None
    valid_until: date | None = None
    created_at: datetime

    class Config:
        from_attributes = True


class DisputeOut(BaseModel):
    id: str
    status: DisputeStatus
    reason: str
    resolution_notes: str | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
