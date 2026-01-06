# Credibility Scoring (Explainable, Rule-Based)

## Principles
- Transparent factors; no AI/ML.
- Time-bound validity; decay for stale claims.
- Multiple independent verifications increase trust.
- Disputes/rejections decrease trust.

## Proposed Factors (example weights)
- Verified organization account: +20
- Verifier role strength (org domain email/verified org): +10
- Duration (0–12 months): +0..15
- Recency (within 12 months): +15; 12–24 months: +10; older: +5
- Evidence quality (public/verifier-only + type): +0..15
- Multiple verifications (second independent verification): +10
- Disputes/rejections: -15 per negative outcome (floor at 0)
- Expiry decay: -10 after validity end; -20 after 6 months expired

## Output
- Total score (0–100, capped).
- Factor breakdown: array of `{factor, score, reason}` for transparency.
- Valid-until date and link status.

## Implementation Notes
- Pure function `calculate_score(claim, verifications)` returning score + breakdown.
- Store breakdown JSON for report rendering.
- Decay applied at request time to avoid stale data exposure.
- Keep weights configurable via env or simple constants for MVP.
