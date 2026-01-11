import aiohttp
import time
from dataclasses import dataclass
from typing import Optional
import streamlit as st
from src.config import OPENWEATHER_API_BASE_URL, CACHE_TTL_SECONDS
from src.services.temperature_analysis_service import CityTemperatureReport
from src.core.logger import logger

@dataclass
class CityWeather:
    temperature: float
    is_anomaly: bool
    error: Optional[str] = None

class CityWeatherFetcher:
    """Получение текущей температуры с кэшем."""

    def __init__(self):
        if 'weather_cache' not in st.session_state:
            st.session_state.weather_cache = {}
            st.session_state.weather_cache_time = {}

    async def get_current_temperature(self, city: str, report: CityTemperatureReport, api_key: str) -> CityWeather:
        key = f"{city}:{api_key}"
        now = time.time()
        if key in st.session_state.weather_cache:
            age = now - st.session_state.weather_cache_time[key]
            if age < CACHE_TTL_SECONDS:
                logger.info(f"Cache hit для {city}")
                return st.session_state.weather_cache[key]

        weather_info = await self._retrieve_temperature(city, report, api_key)
        st.session_state.weather_cache[key] = weather_info
        st.session_state.weather_cache_time[key] = now
        return weather_info

    @staticmethod
    def check_anomaly(temp: float, seasonal_stats, season: str) -> bool:
        mean = seasonal_stats.loc[season, ('temperature', 'mean')]
        std = seasonal_stats.loc[season, ('temperature', 'std')]
        return temp > mean + 2 * std or temp < mean - 2 * std

    @staticmethod
    async def _retrieve_temperature(city: str, report: CityTemperatureReport, api_key: str) -> CityWeather:
        params = {'q': city, 'appid': api_key, 'units': 'metric'}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(OPENWEATHER_API_BASE_URL, params=params) as resp:
                    data = await resp.json()
                    if resp.status == 200:
                        temp = data['main']['temp']
                        season = report.records['season'].iloc[-1]
                        is_anom = CityWeatherFetcher.check_anomaly(temp, report.seasonal_summary, season)
                        return CityWeather(temp, is_anom)
                    return CityWeather(0, False, data.get('message', 'API error'))
        except Exception as e:
            return CityWeather(0, False, f"Ошибка: {str(e)}")
