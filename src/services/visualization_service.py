import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from src.config import FIGURE_SIZE, FIGURE_DPI, TEMPERATURE_COLORS

class TemperatureVisualizationService:
    """Визуализация температурных данных."""

    @staticmethod
    def set_plot_style():
        plt.style.use('seaborn-v0_8-dark-palette')
        sns.set_palette("husl")
        
        # Глобальный размер шрифтов
        plt.rcParams.update({
            'font.size': 18,         # базовый размер шрифта
            'axes.titlesize': 22,    # размер заголовка графика
            'axes.labelsize': 18,    # размер подписи осей
            'xtick.labelsize': 16,   # размер подписей по X
            'ytick.labelsize': 16,   # размер подписей по Y
            'legend.fontsize': 16,   # размер шрифта легенды
        })

    @staticmethod
    def draw_time_series(city_data: pd.DataFrame, city_name: str, ax=None):
        figure, ax = (plt.subplots(figsize=FIGURE_SIZE, dpi=FIGURE_DPI) if ax is None else (ax.figure, ax))
        ax.plot(city_data['timestamp'], city_data['temperature'], color=TEMPERATURE_COLORS['normal'], alpha=0.5, label='Температура')
        ax.plot(city_data['timestamp'], city_data['rolling_avg'], color=TEMPERATURE_COLORS['rolling'], label='Скользящее среднее')
        anomalies = city_data[city_data['is_anomaly']]
        ax.scatter(anomalies['timestamp'], anomalies['temperature'], color=TEMPERATURE_COLORS['anomaly'], label='Аномалии')
        ax.set_title(f"{city_name} — временной ряд температур")
        ax.set_xlabel("Дата")
        ax.set_ylabel("Температура (°C)")
        ax.legend()
        return figure

    @staticmethod
    def draw_season_boxplot(city_data: pd.DataFrame, city_name: str, ax=None):
        figure, ax = (plt.subplots(figsize=FIGURE_SIZE, dpi=FIGURE_DPI) if ax is None else (ax.figure, ax))
        sns.boxplot(data=city_data, x='season', y='temperature', ax=ax)
        ax.set_title(f"{city_name} — распределение температур по сезонам")
        ax.set_ylabel("Температура (°C)")
        return figure

    @staticmethod
    def draw_temperature_histogram(city_data: pd.DataFrame, city_name: str, ax=None):
        figure, ax = (plt.subplots(figsize=FIGURE_SIZE, dpi=FIGURE_DPI) if ax is None else (ax.figure, ax))
        sns.histplot(data=city_data, x='temperature', hue='season', multiple="stack", ax=ax)
        ax.set_title(f"{city_name} — распределение температур")
        ax.set_xlabel("Температура (°C)")
        ax.set_ylabel("Количество дней")
        return figure

    @staticmethod
    def draw_anomaly_heatmap(city_data: pd.DataFrame, city_name: str, ax=None):
        figure, ax = (plt.subplots(figsize=FIGURE_SIZE, dpi=FIGURE_DPI) if ax is None else (ax.figure, ax))
        city_data = city_data.copy()
        city_data['year'] = city_data['timestamp'].dt.year
        city_data['month'] = city_data['timestamp'].dt.month
        pivot = city_data.pivot_table(values='is_anomaly', index='year', columns='month', aggfunc='sum').astype(int)
        sns.heatmap(pivot, ax=ax, cmap='YlOrRd')
        ax.set_title(f"{city_name} — аномалии по месяцам")
        ax.set_xlabel("Месяц")
        ax.set_ylabel("Год")
        return figure