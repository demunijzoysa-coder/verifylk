# Backend — VerifyLK

FastAPI service providing auth, claims, verification, scoring, and report endpoints.

## Quickstart
```bash
python -m venv .venv && . .venv/Scripts/activate  # or source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Env: copy `.env.example` to `.env` and adjust `SECRET_KEY` and `DATABASE_URL` (Postgres in production, SQLite for dev).

## Notable Endpoints (prefixed with /api/v1)
- `POST /auth/register` — register user.
- `POST /auth/login` — login for JWT access/refresh.
- `GET/POST /claims` — create/list candidate claims.
- `POST /claims/{id}/request-verification` — move claim to pending.
- `GET /verifications/inbox` — verifier inbox.
- `POST /verifications/{id}/decision` — approve/reject and recalc score.
- `GET /reports/{token}` — public read-only report (token = claim id in MVP stub).

## Testing
```bash
pytest
```

## Roadmap (backend)
- Replace report token stub with signed links.
- Add evidence upload/presigned URLs.
- Add dispute/admin endpoints and org verification tiers.
- Rate limiting and richer audit logging with sink.
