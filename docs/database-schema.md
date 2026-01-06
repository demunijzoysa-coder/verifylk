# Database Schema (MVP)

Target: PostgreSQL (SQLite for local dev). Timestamps in UTC.

## Tables
### users
- id (uuid, pk)
- email (text, unique)
- password_hash (text)
- full_name (text)
- role (enum: candidate, verifier, employer, admin)
- org_id (fk nullable, for verifiers)
- created_at (timestamptz)
- updated_at (timestamptz)

### organizations
- id (uuid, pk)
- name (text)
- verified_status (enum: unverified, pending, verified)
- contact_email (text)
- contact_phone (text)
- website (text)
- address (text)
- created_at (timestamptz)
- updated_at (timestamptz)

### experience_claims
- id (uuid, pk)
- candidate_id (fk users.id)
- title (text)
- claim_type (enum: internship, apprenticeship, volunteering, informal, freelance, training)
- organization_name (text)
- supervisor_name (text)
- supervisor_contact (text)
- start_date (date)
- end_date (date)
- description (text)
- skill_tags (text[] nullable)
- status (enum: draft, pending, verified, rejected, expired, disputed)
- evidence_visibility (enum: public, verifier_only)
- credibility_score (numeric)
- credibility_breakdown (jsonb)
- created_at (timestamptz)
- updated_at (timestamptz)

### evidence_files
- id (uuid, pk)
- claim_id (fk experience_claims.id)
- file_name (text)
- mime_type (text)
- storage_path (text)
- is_public (bool)
- created_at (timestamptz)

### verification_records
- id (uuid, pk)
- claim_id (fk experience_claims.id)
- verifier_id (fk users.id)
- organization_id (fk organizations.id nullable)
- outcome (enum: approved, rejected)
- notes (text)
- role_type (text)
- verified_start_date (date)
- verified_end_date (date)
- valid_until (date)
- created_at (timestamptz)

### disputes
- id (uuid, pk)
- claim_id (fk experience_claims.id)
- raised_by (fk users.id)
- status (enum: open, under_review, resolved, dismissed)
- reason (text)
- resolution_notes (text)
- created_at (timestamptz)
- updated_at (timestamptz)

### audit_logs
- id (bigserial, pk)
- actor_id (fk users.id nullable for public views)
- action (text)
- entity_type (text)
- entity_id (uuid)
- metadata (jsonb)
- created_at (timestamptz)

## Indexing
- Unique email on users.
- Index on claim status, candidate_id.
- Index on verification_records.claim_id.
- Index on disputes.status.
- Index on audit_logs.entity_type/entity_id for traceability.
