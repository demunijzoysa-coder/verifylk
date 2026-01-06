# API Spec (MVP)

Base URL: `/api/v1`
Auth: JWT access tokens; refresh on `/auth/refresh`.

## Auth
- `POST /auth/register` — register user (email, password, role, org info optional).
- `POST /auth/login` — login and receive tokens.
- `POST /auth/refresh` — refresh access token.

## Candidates
- `GET /me` — current user profile.
- `PUT /me` — update profile basics.
- `POST /claims` — create experience claim.
- `GET /claims` — list candidate claims.
- `GET /claims/{id}` — get claim details (owned).
- `PUT /claims/{id}` — update claim (draft/pending states).
- `POST /claims/{id}/request-verification` — trigger verifier notification.
- `POST /claims/{id}/evidence` — upload evidence metadata (presigned URL flow).

## Verifications
- `GET /verifications/inbox` — pending requests for verifier/org.
- `POST /verifications/{id}/decision` — approve/reject with notes, dates, validity.
- `GET /verifications/history` — past verifications by verifier/org.

## Reports
- `GET /reports/{token}` — public read-only report with verified claims and score breakdown.

## Admin
- `GET /admin/disputes` — list disputes.
- `POST /admin/disputes/{id}/decision` — resolve/dismiss dispute.
- `GET /admin/audit` — paginated audit logs.
- `POST /admin/orgs/{id}/verify` — update org verification status.

## Response Shapes (examples)
`ExperienceClaim`
```json
{
  "id": "uuid",
  "title": "Volunteer Coordinator",
  "type": "volunteering",
  "organization_name": "Community Org",
  "supervisor_name": "Jane Doe",
  "supervisor_contact": "jane@org.lk",
  "start_date": "2024-01-01",
  "end_date": "2024-06-01",
  "description": "Led... ",
  "skill_tags": ["coordination", "fundraising"],
  "evidence": [
    {"id": "uuid", "file_name": "letter.pdf", "mime_type": "application/pdf", "is_public": true}
  ],
  "status": "verified",
  "credibility_score": 86,
  "credibility_breakdown": [
    {"factor": "verified_org", "score": 20, "reason": "Org verified"},
    {"factor": "recency", "score": 15, "reason": "Completed within last 12 months"}
  ],
  "created_at": "2024-01-01T10:00:00Z",
  "updated_at": "2024-06-02T08:00:00Z"
}
```

`VerificationRecord`
```json
{
  "id": "uuid",
  "claim_id": "uuid",
  "outcome": "approved",
  "notes": "Confirmed hours and outputs.",
  "role_type": "Supervisor",
  "verified_start_date": "2024-01-01",
  "verified_end_date": "2024-06-01",
  "valid_until": "2026-06-01",
  "created_at": "2024-06-02T08:00:00Z"
}
```
