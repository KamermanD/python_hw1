import sys
from loguru import logger

from src.core.log_config import LOG_CONFIG


# создаём директории
LOG_CONFIG.directory.mkdir(exist_ok=True)
(LOG_CONFIG.directory / "archive").mkdir(exist_ok=True)

logger.remove()

# Консоль
logger.add(
    sys.stdout,
    format=LOG_CONFIG.format,
    level=LOG_CONFIG.level,
    colorize=True
)

# Основной лог
logger.add(
    LOG_CONFIG.directory / "app.log",
    format=LOG_CONFIG.format,
    level=LOG_CONFIG.level,
    rotation=LOG_CONFIG.rotation,
    retention=LOG_CONFIG.retention,
    compression="zip",
    encoding="utf-8"
)

# Ошибки
logger.add(
    LOG_CONFIG.directory / "errors.log",
    format=LOG_CONFIG.format,
    level="ERROR",
    rotation="1 week",
    retention=LOG_CONFIG.retention,
    compression="zip",
    encoding="utf-8",
    backtrace=True,
    diagnose=True
)