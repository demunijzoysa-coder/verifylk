# Local Credential & Experience Verification System (Sri Lanka) — Concept (In Development)

Evidence-backed, human-verified experience proof for internships, apprenticeships, volunteering, informal work, and NGO placements in Sri Lanka. This is an active development concept; expect changes as workflows and endpoints mature.

## Why
- Sri Lanka’s informal and community work is hard to prove; references are inconsistent or unreachable.
- Employers and programs spend time validating claims and still face fraud risk.
- Youth and rural candidates lose opportunities because they cannot provide trusted evidence.

## What
- Verified endorsements from organizations/supervisors with time-bound validity.
- Evidence-backed claims with audit logs and dispute handling.
- Explainable, rules-based credibility scoring (no black box).
- Shareable verification reports with signed, tamper-resistant links.

## Roles & Scope (MVP in progress)
- Candidate: create claims, upload evidence, request verification, share reports.
- Verifier: inbox, approve/reject with notes, confirm dates/role.
- Employer: read-only report with score breakdown.
- Admin: org verification toggle, dispute decisions, audit view (early stage).

## Architecture (current)
- Frontend: Vite + React + TypeScript; role-based UI and report view.
- Backend: FastAPI (Python), JWT auth scaffold, SQLAlchemy (Postgres-ready; SQLite for dev), S3/email placeholders.
- Config: `.env` driven; signed links and audit/rate-limit stubs.

## Repository layout
- `backend/` — FastAPI service, domain models, scoring, routes.
- `frontend/` — Vite React client with role flows and report UI.
- `docs/` — PRD, architecture, API spec, data schema, pilot plan.

## Run locally
Prereqs: Python 3.11+, Node 18+, npm, Git.

Backend:
```bash
cd backend
python -m venv .venv && . .venv/Scripts/activate  # or source .venv/bin/activate on macOS/Linux
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
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

## One-command start
- Windows: `.\start.ps1` (add `-SkipInstall` after first run)
- macOS/Linux: `./start.sh` (use `--skip-install` after first run)
Starts backend (8000) and frontend (5173) in separate terminals.

## One-command stop
- Windows: `.\stop.ps1`
- macOS/Linux: `./stop.sh`
Attempts to stop processes on ports 8000 and 5173; close any remaining dev terminals if still running.

## Accounts and login
- Seeded admin (for testing): `admin@gmail.com` / `1234` (role `admin`). Created automatically on backend start.
- Register other roles (candidate, verifier, employer) via the auth overlay. Tokens persist in the browser until you log out.

## What the UI does today
- Auth overlay: login/register first; stays signed in until logout.
- Candidate: create claims, request verification, view statuses/scores.
- Verifier: inbox to approve/reject requests.
- Employer: fetch a report by token (MVP uses claim id as token).
- Admin: org verification toggle, disputes resolve/dismiss, audit log list (seeded orgs/sample data; evolving).

## API quick links
- Swagger: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
- Health: http://127.0.0.1:8000/api/v1/health

## Roadmap (phased)
- Phase 1: MVP flows, scoring, report links, moderation & dispute basics.
- Phase 2: Org verification tiers, bulk verification, QR cards, employer API, SMS support.
- Phase 3: Ecosystem integrations with NGOs/training centers and scholarship/recruitment pipelines.

## Status
Work in progress. Commits are granular to keep the build traceable.
