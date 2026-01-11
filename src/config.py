import os
from pathlib import Path
from typing import Final
from dotenv import load_dotenv
from src.core.logger import logger
from src.core.log_config import ROOT_PROJ

# Загружаем переменные из .env
load_dotenv()
logger.info("Конфигурация из .env загружена")

# Пути к данным
DATA_DIR: Final[Path] = ROOT_PROJ / "data"

# API OpenWeatherMap
OPENWEATHER_API_KEY: Final[str] = os.getenv("OPENWEATHER_API_KEY", "")
OPENWEATHER_API_BASE_URL: Final[str] = "http://api.openweathermap.org/data/2.5/weather"

# Настройки анализа температур
ROLLING_WINDOW_DAYS: Final[int] = 30
ANOMALY_STD_FACTOR: Final[float] = 2.0
DEFAULT_CITY: Final[str] = "Moscow"

# Настройки визуализации
FIGURE_SIZE: Final[tuple] = (20, 15)
FIGURE_DPI: Final[int] = 100
TEMPERATURE_COLORS: Final[dict] = {
    'normal': '#1f77b4',
    'anomaly': '#d62728',
    'rolling': '#ff7f0e'
}

# Кэширование результатов API
CACHE_TTL_SECONDS: Final[int] = 300  # 5 минут