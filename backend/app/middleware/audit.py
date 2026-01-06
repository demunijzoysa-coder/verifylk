import logging
import time
from typing import Callable

from fastapi import Request

logger = logging.getLogger("verifylk.audit")


async def audit_middleware(request: Request, call_next: Callable):
    start = time.time()
    response = await call_next(request)
    duration = round((time.time() - start) * 1000, 2)
    logger.info(
        "request",
        extra={
            "path": request.url.path,
            "method": request.method,
            "status": response.status_code,
            "duration_ms": duration,
            "client": request.client.host if request.client else None,
        },
    )
    return response
