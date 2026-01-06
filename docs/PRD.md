# Product Requirements — Local Credential & Experience Verification (Sri Lanka)

## Vision
A human-verified, evidence-backed layer that lets candidates prove internships, apprenticeships, volunteering, informal and freelance work with credible endorsements, audit trails, and time-bound validity. No blockchain, no AI black boxes.

## Users & Roles
- **Candidate**: creates profile and experience claims, uploads evidence, requests verification, shares reports.
- **Verifier (Org/Supervisor)**: receives requests, approves/rejects with notes, confirms dates/role, optionally attaches proof, maintains org profile.
- **Employer/Program (Viewer)**: views read-only reports, credibility breakdown, validates authenticity.
- **Admin**: moderation, disputes, abuse detection, org verification status, audit logs.

## Problem Statement
- Informal work and community volunteering lack credible proof.
- References are inconsistent/unreachable; employers waste time verifying.
- Youth/rural candidates lose opportunities; fraud risk stays high.

## Goals
- Reduce verification friction and fraud risk.
- Provide explainable credibility scoring.
- Make verifiable reports easy to share and validate.

## Non-Goals (Phase 1)
- Job marketplace.
- Blockchain credentials.
- Heavy KYC/government integration.
- AI scoring.

## Functional Requirements (MVP)
### Candidate
- Sign up/login.
- Create/edit experience claims with type, org, supervisor contact, dates, description, skills tags.
- Upload evidence attachments.
- Request verification (email link or org dashboard).
- Generate shareable, signed report link.

### Verifier
- Org account creation.
- Verification inbox with pending requests.
- Approve/reject with notes; confirm dates/role type; optional proof attachment.
- View verified candidates/claims history.

### Employer/Viewer
- Read-only verification report.
- See verification details and score breakdown.
- Validate link authenticity; request additional confirmation optionally.

### Admin
- Moderation dashboard.
- Dispute workflow (flag → review → decision).
- Audit logs of key actions.
- Manage org verification status.

## Data Objects
- **Experience Claim**: id, candidate id, title, type, organization name, supervisor name/contact, start/end dates, description, skill tags, evidence attachments, status (draft/pending/verified/rejected/expired/disputed).
- **Verification Record**: verifier identity/org, verified dates, role type, outcome + notes, timestamp, valid-until date, audit metadata.
- **Credibility Score**: rule-based factors (org verified, verifier role strength, duration, recency, evidence quality, multiple verifications, disputes/rejections).
- **Audit Log**: actor, action, entity, timestamp, metadata.

## Credibility Scoring Principles
- Transparent, rule-based, explainable factors.
- Time-bound validity; stale claims decay.
- Penalties for disputes/rejections.

## Workflows
1. Candidate creates claim → adds evidence → requests verification.
2. Verifier receives request → confirms/rejects with notes → sets validity.
3. Claim status updates → score recalculates.
4. Candidate shares report link → employer views read-only report.
5. Admin handles disputes and moderation; audit logs capture actions.

## Security & Privacy
- JWT auth with refresh tokens.
- Signed, tamper-resistant share links.
- Evidence visibility controls: public in report vs verifier-only.
- Rate limiting & abuse detection placeholders.
- Evidence file type/size checks.
- GDPR-like principles: purpose limitation, minimization, deletion policy.

## Constraints & Assumptions
- Postgres primary datastore (dev may use SQLite).
- S3-compatible storage for evidence.
- Email provider for verification requests.
- Sri Lanka connectivity realities; keep flows low bandwidth.

## Success Metrics (MVP)
- Orgs onboarded.
- Verification completion rate; median time to verify.
- Employer views per verified report.
- Fraud/rejection rate trends.
- Outcomes enabled (internships/jobs/scholarships).
