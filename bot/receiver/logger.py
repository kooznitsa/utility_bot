import os
import logging
from logging.handlers import RotatingFileHandler

from config_data.config import settings


def gateway_api_driver_logger_init() -> logging.Logger:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    if not os.path.exists(settings.logs_dir):
        os.makedirs(settings.logs_dir)

    rfh = RotatingFileHandler(
        encoding='utf-8',
        filename=f'{settings.logs_dir}{settings.GatewayAPIDriverLogger.filename}',
        maxBytes=settings.GatewayAPIDriverLogger.max_bytes,
        backupCount=settings.GatewayAPIDriverLogger.backup_count,
    )
    rfh.setFormatter(settings.GatewayAPIDriverLogger.formatter)
    logger.addHandler(rfh)

    return logger
