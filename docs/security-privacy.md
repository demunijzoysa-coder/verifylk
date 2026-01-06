# Security, Privacy, and Abuse Controls

## Security
- JWT auth with refresh; short-lived access tokens.
- Role-based access control (candidate, verifier, employer, admin).
- Signed share links with expiry; token audience/issuer validation.
- File upload validation: size/type whitelist; future AV scan hook.
- Rate limiting for auth, claim creation, verification actions.
- Audit logging for sensitive actions (claim changes, verifications, disputes, admin actions).

## Privacy
- Evidence visibility: public in report vs verifier-only; default to verifier-only.
- Minimal personal data; avoid collecting sensitive info.
- Explicit consent wording for verifiers.
- Data retention: delete evidence on claim deletion; clear policy for disputes.
- GDPR-like principles: purpose limitation, minimization, access/deletion rights.

## Abuse & Fraud Mitigation (MVP)
- Org verification tiers; manual approval for org badges.
- Throttling verification requests to prevent spam.
- Anomaly hooks (multiple rejections, IP/device metadata captured later).
- Dispute workflow with auditability.

## Operational Practices
- Environment-based secrets management via `.env`.
- Separate dev/staging/prod credentials and storage buckets.
- Centralized logging for moderation review.
