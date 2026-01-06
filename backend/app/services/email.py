from logging import getLogger

logger = getLogger(__name__)


def send_verification_request_email(to_email: str, claim_id: str, candidate_name: str, link: str) -> None:
    """Stub for transactional email; logs until provider configured."""
    logger.info("Send verification email", extra={"to": to_email, "claim_id": claim_id, "candidate": candidate_name, "link": link})
