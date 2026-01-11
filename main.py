import asyncio
import pandas as pd

from src.config import DATA_DIR, DEFAULT_CITY, OPENWEATHER_API_KEY
from src.services.temperature_analysis_service import TemperatureAnalysisService
from src.services.city_weather_service import CityWeatherFetcher
from src.core.logger import logger


async def print_temperature_info(city: str, weather_info: CityWeatherFetcher):
    if weather_info.error:
        logger.error(f"Ошибка при получении температуры: {weather_info.error}")
        return

    status = "аномальная" if weather_info.is_anomaly else "нормальная"
    logger.info(
        f"Текущая температура в {city}: {weather_info.temperature}°C ({status})"
    )


async def print_city_analysis(city: str, report):
    logger.info(f"Анализ для города {city}:")
    logger.info(f"Сезонная статистика:\n{report.seasonal_summary}")
    logger.info(f"Количество аномалий: {report.anomaly_count}")


async def main():
    data_path = DATA_DIR / "temperature_data.csv"
    logger.info(f"Загрузка данных из {data_path}")
    df = pd.read_csv(data_path)
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    analyses = await TemperatureAnalysisService.analyze_all_cities(df)

    city = DEFAULT_CITY
    city_report = analyses[city]

    await print_city_analysis(city, city_report)

    weather_service = CityWeatherFetcher()
    current_weather = await weather_service.get_current_temperature(
        city,
        city_report,
        OPENWEATHER_API_KEY
    )

    await print_temperature_info(city, current_weather)


if __name__ == "__main__":
    asyncio.run(main())