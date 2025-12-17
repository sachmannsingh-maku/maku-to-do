import logging
from fastapi import Request
from fastapi.responses import JSONResponse

logger = logging.getLogger("error")

async def global_exception_handler(
    request: Request,
    exc: Exception,
):
    logger.exception(
        "unhandled_exception path=%s",
        request.url.path,
    )

    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )
