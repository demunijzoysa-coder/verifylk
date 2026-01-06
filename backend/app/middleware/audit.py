import time
from typing import Callable

from fastapi import Request


async def audit_middleware(request: Request, call_next: Callable):
    start = time.time()
    response = await call_next(request)
    duration = round((time.time() - start) * 1000, 2)
    request.app.logger.info(
        "audit",
        extra={
            "path": request.url.path,
            "method": request.method,
            "status": response.status_code,
            "duration_ms": duration,
            "client": request.client.host if request.client else None,
        },
    )
    return response
