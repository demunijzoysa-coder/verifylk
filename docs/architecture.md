# System Architecture

## Overview
- **Frontend**: Vite + React + TypeScript, role-based UI (Candidate, Verifier, Employer, Admin), report view with signed token validation.
- **Backend**: FastAPI with JWT auth scaffold, SQLAlchemy models targeting Postgres (SQLite for local dev), service layer for scoring and verification flows.
- **Storage**: S3-compatible bucket for evidence; signed URLs or presigned uploads (MVP uses stub/local path).
- **Email**: Transactional provider for verification requests; adapter interface for swapping providers.
- **Auth**: JWT access + refresh tokens; role-based permissions (Candidate/Verifier/Employer/Admin).
- **Security**: Rate-limit placeholders, audit logging, signed share links, file type/size validation.

## Key Services (backend)
- **Auth Service**: user registration/login, token issuance, role enforcement.
- **Claims Service**: CRUD for experience claims, evidence metadata, status transitions.
- **Verification Service**: inbox, approve/reject, validity window, audit trail updates.
- **Scoring Service**: rule-based credibility computation and explanation.
- **Report Service**: public read-only view of verified claims via signed tokens/links.
- **Moderation Service**: disputes and admin actions.

## Data Flow (high level)
1. Candidate submits claim with evidence metadata.
2. Candidate requests verification; system emails verifier with signed link or surfaces in org inbox.
3. Verifier approves/rejects with notes; claim status updates; score recomputes.
4. Candidate shares report link with employer; employer fetches read-only data and score breakdown.
5. Admin can flag/dispute actions; audit log records all sensitive events.

## Components & Boundaries
- **API Layer**: FastAPI routers for each domain; dependency-injected services.
- **Persistence**: SQLAlchemy models + repositories; easy swap of DB URL.
- **Storage Adapter**: abstracted S3 client; local file stub for dev.
- **Email Adapter**: provider-agnostic interface; console/log stub for dev.
- **Scoring Engine**: pure functions with factor contributions + explanations.
- **Audit Logger**: middleware capturing actor, action, entity, timestamp, IP (if available).

## Deployment (future-ready)
- Container-friendly; 12-factor config via `.env`.
- Separate frontend and backend services; CDN for static assets.
- Postgres + S3 + transactional email (e.g., SES/SendGrid) + log sink (e.g., Loki/ELK).

## Risk & Mitigation
- **Fraud/abuse**: rate limits, org verification tiers, anomaly flags (hooks stubbed).
- **Privacy**: evidence visibility controls, minimal data retention.
- **Reliability**: background retries for email, idempotent verification endpoints.
