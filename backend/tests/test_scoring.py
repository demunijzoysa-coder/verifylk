from datetime import date

from app.models import ClaimStatus, EvidenceVisibility, ExperienceClaim, VerificationOutcome, VerificationRecord
from app.services.scoring import calculate_score


def test_calculate_score_for_recent_verified_claim():
    claim = ExperienceClaim(
        id="c1",
        candidate_id="u1",
        title="Test Claim",
        claim_type="internship",
        organization_name="Org",
        supervisor_name="Jane",
        supervisor_contact="jane@org.lk",
        start_date=date(2024, 1, 1),
        end_date=date(2024, 6, 1),
        description="Did real work",
        skill_tags=["coordination"],
        status=ClaimStatus.verified,
        evidence_visibility=EvidenceVisibility.public,
    )
    verification = VerificationRecord(
        id="v1",
        claim_id="c1",
        verifier_id="verifier-1",
        organization_id=None,
        outcome=VerificationOutcome.approved,
        notes=None,
        role_type="Supervisor",
        verified_start_date=date(2024, 1, 1),
        verified_end_date=date(2024, 6, 1),
        valid_until=date(2026, 6, 1),
    )
    score, breakdown = calculate_score(claim, [verification])
    assert score > 0
    assert any(item.factor == "recency" for item in breakdown)


def test_non_verified_claim_scores_zero():
    claim = ExperienceClaim(
        id="c2",
        candidate_id="u1",
        title="Draft Claim",
        claim_type="volunteering",
        organization_name="Org",
        supervisor_name="Jane",
        supervisor_contact="jane@org.lk",
        start_date=date(2023, 1, 1),
        end_date=date(2023, 2, 1),
        description="Draft only",
        skill_tags=[],
        status=ClaimStatus.draft,
        evidence_visibility=EvidenceVisibility.verifier_only,
    )
    score, breakdown = calculate_score(claim, [])
    assert score == 0
    assert breakdown[0].reason == "Claim not verified"
