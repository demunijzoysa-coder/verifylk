from logging import getLogger

logger = getLogger(__name__)


def get_presigned_upload_url(file_name: str, mime_type: str) -> dict:
    """Stub for S3-compatible presigned upload URLs."""
    logger.info("Presign upload", extra={"file_name": file_name, "mime_type": mime_type})
    return {
        "url": "https://example-bucket.s3.local/upload",
        "fields": {"key": file_name, "Content-Type": mime_type},
    }
