import enum
from datetime import datetime, date
from typing import List

from sqlalchemy import Boolean, Column, Date, DateTime, Enum, ForeignKey, JSON, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import uuid4

from ..db import Base


def uuid_default():
    return str(uuid4())


class UserRole(str, enum.Enum):
    candidate = "candidate"
    verifier = "verifier"
    employer = "employer"
    admin = "admin"


class OrgStatus(str, enum.Enum):
    unverified = "unverified"
    pending = "pending"
    verified = "verified"


class ClaimStatus(str, enum.Enum):
    draft = "draft"
    pending = "pending"
    verified = "verified"
    rejected = "rejected"
    expired = "expired"
    disputed = "disputed"


class EvidenceVisibility(str, enum.Enum):
    public = "public"
    verifier_only = "verifier_only"


class VerificationOutcome(str, enum.Enum):
    approved = "approved"
    rejected = "rejected"


class DisputeStatus(str, enum.Enum):
    open = "open"
    under_review = "under_review"
    resolved = "resolved"
    dismissed = "dismissed"


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=uuid_default)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String)
    full_name: Mapped[str] = mapped_column(String)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole))
    org_id: Mapped[str | None] = mapped_column(String, ForeignKey("organizations.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    organization: Mapped["Organization"] = relationship(back_populates="members")


class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=uuid_default)
    name: Mapped[str] = mapped_column(String)
    verified_status: Mapped[OrgStatus] = mapped_column(Enum(OrgStatus), default=OrgStatus.unverified)
    contact_email: Mapped[str | None] = mapped_column(String, nullable=True)
    contact_phone: Mapped[str | None] = mapped_column(String, nullable=True)
    website: Mapped[str | None] = mapped_column(String, nullable=True)
    address: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    members: Mapped[List[User]] = relationship(back_populates="organization")
    verifications: Mapped[List["VerificationRecord"]] = relationship(back_populates="organization")


class ExperienceClaim(Base):
    __tablename__ = "experience_claims"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=uuid_default)
    candidate_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String)
    claim_type: Mapped[str] = mapped_column(String)
    organization_name: Mapped[str] = mapped_column(String)
    supervisor_name: Mapped[str] = mapped_column(String)
    supervisor_contact: Mapped[str] = mapped_column(String)
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[date] = mapped_column(Date)
    description: Mapped[str] = mapped_column(Text)
    skill_tags: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
    status: Mapped[ClaimStatus] = mapped_column(Enum(ClaimStatus), default=ClaimStatus.draft)
    evidence_visibility: Mapped[EvidenceVisibility] = mapped_column(Enum(EvidenceVisibility), default=EvidenceVisibility.verifier_only)
    credibility_score: Mapped[float | None] = mapped_column(Numeric, nullable=True)
    credibility_breakdown: Mapped[list | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    evidence: Mapped[List["EvidenceFile"]] = relationship(back_populates="claim")
    verifications: Mapped[List["VerificationRecord"]] = relationship(back_populates="claim")


class EvidenceFile(Base):
    __tablename__ = "evidence_files"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=uuid_default)
    claim_id: Mapped[str] = mapped_column(String, ForeignKey("experience_claims.id"))
    file_name: Mapped[str] = mapped_column(String)
    mime_type: Mapped[str] = mapped_column(String)
    storage_path: Mapped[str] = mapped_column(String)
    is_public: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    claim: Mapped[ExperienceClaim] = relationship(back_populates="evidence")


class VerificationRecord(Base):
    __tablename__ = "verification_records"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=uuid_default)
    claim_id: Mapped[str] = mapped_column(String, ForeignKey("experience_claims.id"))
    verifier_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"))
    organization_id: Mapped[str | None] = mapped_column(String, ForeignKey("organizations.id"), nullable=True)
    outcome: Mapped[VerificationOutcome] = mapped_column(Enum(VerificationOutcome))
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    role_type: Mapped[str | None] = mapped_column(String, nullable=True)
    verified_start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    verified_end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    valid_until: Mapped[date | None] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    claim: Mapped[ExperienceClaim] = relationship(back_populates="verifications")
    organization: Mapped[Organization | None] = relationship(back_populates="verifications")


class Dispute(Base):
    __tablename__ = "disputes"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=uuid_default)
    claim_id: Mapped[str] = mapped_column(String, ForeignKey("experience_claims.id"))
    raised_by: Mapped[str] = mapped_column(String, ForeignKey("users.id"))
    status: Mapped[DisputeStatus] = mapped_column(Enum(DisputeStatus), default=DisputeStatus.open)
    reason: Mapped[str] = mapped_column(Text)
    resolution_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    actor_id: Mapped[str | None] = mapped_column(String, nullable=True)
    action: Mapped[str] = mapped_column(String)
    entity_type: Mapped[str] = mapped_column(String)
    entity_id: Mapped[str] = mapped_column(String)
    metadata: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
