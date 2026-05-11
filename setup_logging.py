import logging
from settings import settings


def setup_logging():
    level = settings.LOG_LEVEL.upper()
    logging.basicConfig(
        level=getattr(logging, level, logging.INFO),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
