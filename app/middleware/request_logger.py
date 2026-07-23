import time

from loguru import logger


async def log_requests(
        request,
        call_next
):

    start = time.time()

    response = await call_next(
        request
    )

    duration = (
        time.time() - start
    )

    logger.info(
        f"{request.method} "
        f"{request.url.path} "
        f"{response.status_code} "
        f"{duration:.3f}s"
    )

    return response