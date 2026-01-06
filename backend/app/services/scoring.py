from datetime import date
from typing import Iterable, Tuple

from ..models import ClaimStatus, ExperienceClaim, VerificationRecord
from ..schemas.models import ScoreBreakdown


def _months_between(start: date, end: date) -> int:
    return max(0, (end.year - start.year) * 12 + (end.month - start.month))


def calculate_score(claim: ExperienceClaim, verifications: Iterable[VerificationRecord]) -> Tuple[float, list[ScoreBreakdown]]:
    """Rule-based scoring. Returns (score, breakdown)."""
    total = 0.0
    breakdown: list[ScoreBreakdown] = []
    today = date.today()

    verifications = list(verifications)
    verified_count = len(verifications)

    # Base requirement: only consider verified claims
    if claim.status != ClaimStatus.verified:
        return 0, [ScoreBreakdown(factor="status", score=0, reason="Claim not verified")]

    # Recency factor
    months_since_end = _months_between(claim.end_date, today)
    if months_since_end <= 12:
        score = 15
        reason = "Completed within last 12 months"
    elif months_since_end <= 24:
        score = 10
        reason = "Completed within last 24 months"
    else:
        score = 5
        reason = "Completed more than 2 years ago"
    total += score
    breakdown.append(ScoreBreakdown(factor="recency", score=score, reason=reason))

    # Duration factor
    duration_months = _months_between(claim.start_date, claim.end_date) or 1
    dur_score = min(15, duration_months)  # cap at 15
    breakdown.append(ScoreBreakdown(factor="duration", score=dur_score, reason=f"{duration_months} months recorded"))
    total += dur_score

    # Evidence visibility factor
    if claim.evidence_visibility.value == "public":
        ev_score = 10
        breakdown.append(ScoreBreakdown(factor="evidence", score=ev_score, reason="Public evidence provided"))
        total += ev_score
    else:
        ev_score = 5
        breakdown.append(ScoreBreakdown(factor="evidence", score=ev_score, reason="Evidence available to verifiers"))
        total += ev_score

    # Verification count factor
    if verified_count >= 2:
        v_score = 20
        reason = "Multiple independent verifications"
    elif verified_count == 1:
        v_score = 15
        reason = "Single verification completed"
    else:
        v_score = 0
        reason = "No verifications recorded"
    total += v_score
    breakdown.append(ScoreBreakdown(factor="verifications", score=v_score, reason=reason))

    # Validity windows
    expired = any(v.valid_until and v.valid_until < today for v in verifications)
    if expired:
        penalty = -10
        total += penalty
        breakdown.append(ScoreBreakdown(factor="expiry", score=penalty, reason="Verification validity expired"))

    # Normalize: cap between 0 and 100
    total = max(0.0, min(100.0, total))
    return total, breakdown
