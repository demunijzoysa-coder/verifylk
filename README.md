# Local Credential & Experience Verification System (Sri Lanka)

Human-verified, evidence-backed experience verification for internships, apprenticeships, volunteering, informal work, and NGO placements in Sri Lanka. The goal is to help candidates prove experience, help verifiers respond efficiently, and give employers a trusted, explainable view of credibility.

## Problem
- Informal and community work is hard to prove; references are inconsistent or unreachable.
- Employers and programs spend time validating claims and still face fraud risk.
- Youth and rural candidates lose opportunities because they cannot provide trusted evidence.

## Solution
- Verified endorsements from organizations/supervisors with time-bound validity.
- Evidence-backed claims with audit logs and dispute handling.
- Explainable, rules-based credibility scoring (no black box).
- Shareable verification reports with signed, tamper-resistant links.

## MVP Scope (Phase 1)
- Roles: Candidate, Verifier (organization/supervisor), Employer (viewer), Admin.
- Candidate: profile, experience claims, evidence upload, verification requests, shareable report.
- Verifier: inbox, approve/reject with notes, confirm dates/role, optional proof attachment.
- Employer: read-only report with verification details and score breakdown.
- Admin: moderation basics, dispute workflow, audit logs.

## Architecture (planned)
- Frontend: Vite + React + TypeScript, role-based UI, report view.
- Backend: FastAPI (Python) with JWT auth scaffold, Postgres-ready via SQLAlchemy (dev uses SQLite), S3-compatible storage placeholders, email hook.
- Infrastructure: `.env` driven config, rate-limit and audit stubs, signed share tokens.

## Repository layout (incremental)
- `backend/` — FastAPI service, domain models, scoring, routes.
- `frontend/` — Vite React client with role flows and report UI.
- `docs/` — PRD, architecture, API spec, data schema, pilot plan.

## Getting started
Prereqs: Python 3.11+, Node 18+, npm, Git.

Backend:
```bash
cd backend
python -m venv .venv && . .venv/Scripts/activate  # use `source .venv/bin/activate` on macOS/Linux
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Frontend:
```bash
cd frontend
npm install
npm run dev
```

Tests:
```bash
cd backend
pytest
```

Key docs:
- docs/PRD.md — product requirements
- docs/architecture.md — system design
- docs/database-schema.md — tables
- docs/api-spec.md — endpoints
- docs/scoring.md — scoring rules

## One-command launcher
- Windows: `.\start.ps1` (add `-SkipInstall` after first run to speed up)
- macOS/Linux: `./start.sh` (use `--skip-install` after first run)

This starts backend (FastAPI on 8000) and frontend (Vite on 5173) in separate terminals.

## Roadmap (phased)
- Phase 1: MVP flows, scoring, report links, moderation & dispute basics.
- Phase 2: Org verification tiers, bulk verification, QR cards, employer API, SMS support.
- Phase 3: Ecosystem integrations with NGOs/training centers and scholarship/recruitment pipelines.

## Status
Work in progress. Commits are granular to keep the build traceable.
