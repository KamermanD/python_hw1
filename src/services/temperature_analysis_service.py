from dataclasses import dataclass
from typing import Dict
import pandas as pd
from src.config import ROLLING_WINDOW_DAYS, ANOMALY_STD_FACTOR

@dataclass
class CityTemperatureReport:
    city_name: str
    seasonal_summary: pd.DataFrame
    records: pd.DataFrame
    anomaly_count: int

class TemperatureAnalysisService:
    """Сервис анализа температурных данных по городам."""

    @staticmethod
    async def analyze_all_cities(df: pd.DataFrame) -> Dict[str, CityTemperatureReport]:
        """Анализ температур для всех городов."""
        reports = {}
        for city in df['city'].unique():
            reports[city] = await TemperatureAnalysisService.analyze_single_city(df, city)
        return reports

    @staticmethod
    async def analyze_single_city(df: pd.DataFrame, city: str) -> CityTemperatureReport:
        """Анализ температурных данных для одного города."""
        city_df = df[df['city'] == city].copy()
        city_df['rolling_avg'] = city_df['temperature'].rolling(window=ROLLING_WINDOW_DAYS, center=True).mean()

        seasonal_stats = city_df.groupby('season').agg({
            'temperature': ['mean', 'std']
        }).round(2)

        city_df['is_anomaly'] = False
        for season in seasonal_stats.index:
            mask = city_df['season'] == season
            stats = seasonal_stats.loc[season]
            city_df.loc[mask, 'is_anomaly'] = (
                (city_df.loc[mask, 'temperature'] > stats[('temperature', 'mean')] + ANOMALY_STD_FACTOR * stats[('temperature', 'std')]) |
                (city_df.loc[mask, 'temperature'] < stats[('temperature', 'mean')] - ANOMALY_STD_FACTOR * stats[('temperature', 'std')])
            )

        return CityTemperatureReport(
            city_name=city,
            seasonal_summary=seasonal_stats,
            records=city_df,
            anomaly_count=city_df['is_anomaly'].sum()
        )