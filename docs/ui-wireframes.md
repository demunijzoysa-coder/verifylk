# UI Wireframe Notes (Text-first)

## Candidate
- **Dashboard**: status of claims (draft/pending/verified/rejected/expired), CTA to add claim.
- **New Claim Form**: title, type, org, supervisor contact, dates, description prompts, skill tags, evidence upload, visibility selector.
- **Request Verification**: pick verifier (email/org), send request, show pending badge.
- **Report Links**: list signed links, regenerate/expire, copy to clipboard.

## Verifier
- **Inbox**: pending requests with candidate name, org, role, dates, evidence preview, accept/reject buttons.
- **Decision Modal**: confirm dates/role type, outcome, notes, validity end date, optional proof attachment.
- **History**: past verifications, filters by org/status.

## Employer/Viewer
- **Report View**: candidate summary, verified claims list, verification details, credibility score with factor breakdown, evidence (public-only), link validity badge.
- **Validation**: token status (valid/expired/tampered).

## Admin
- **Moderation/Disputes**: list of flagged claims, decision controls, audit trail.
- **Org Verification**: list orgs, verify/reject, badge status.
- **Audit Logs**: filterable events.

## Visual Style (guidance)
- Clean, trust-first, avoid dark patterns.
- Clear separation of verified vs pending vs rejected states.
- Prominent credibility score with “why” breakdown.
- Evidence visibility badges (public/verifier-only).
