import logging
import time
from fastapi import Request

logger = logging.getLogger("request")

async def log_requests(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time

    logger.info(
        "method=%s path=%s status=%s duration=%.3f",
        request.method,
        request.url.path,
        response.status_code,
        process_time,
    )

    return response
