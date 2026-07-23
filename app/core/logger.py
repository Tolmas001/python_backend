from loguru import logger


logger.add(
    "storage/requests.log",
    rotation="10 MB",
    level="INFO"
)
