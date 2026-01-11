import streamlit as st
import asyncio
from src.services.temperature_analysis_service import TemperatureAnalysisService
from src.services.city_weather_service import CityWeatherFetcher
from src.services.visualization_service import TemperatureVisualizationService
from src.utils.data_utils import read_csv_async
from src.config import DEFAULT_CITY, OPENWEATHER_API_KEY
from src.core.logger import logger

st.cache_data.clear()

async def main():
    st.title("Анализ температурных данных")

    uploaded_file = st.file_uploader("Загрузите файл CSV", type=["csv"])

    if uploaded_file:
        success, message, df = await read_csv_async(uploaded_file)
        if not success:
            st.error(message)
            st.stop()

        st.success(message)

        cities = df['city'].unique()
        selected_city = st.selectbox(
            "Выберите город",
            options=cities,
            index=list(cities).index(DEFAULT_CITY) if DEFAULT_CITY in cities else 0
        )

        city_report = await TemperatureAnalysisService.analyze_single_city(df, selected_city)

        api_key = st.text_input(
            "API ключ OpenWeatherMap",
            value=OPENWEATHER_API_KEY,
            type="password"
        )

        if api_key:
            weather = await CityWeatherFetcher().get_current_temperature(
                selected_city,
                city_report,
                api_key
            )

            if weather.error:
                st.error(f"Ошибка: {weather.error}")
                logger.error(weather.error)
                st.stop()

            display_results(city_report, weather)
            display_stats(city_report)


def display_results(report, weather_info):
    st.subheader("Текущая температура")
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            label=report.city_name,
            value=f"{weather_info.temperature}°C",
            delta="Аномальная" if weather_info.is_anomaly else "Нормальная",
            delta_color="inverse" if weather_info.is_anomaly else "normal"
        )

    with col2:
        current_season = report.records['season'].iloc[-1]
        season_stats = report.seasonal_summary.loc[current_season]
        st.caption("Статистика текущего сезона:")
        st.info(
            f"**{current_season.title()}**\n"
            f"- Средняя: {season_stats[('temperature','mean')]:.1f}°C\n"
            f"- Стандартное отклонение: {season_stats[('temperature','std')]:.1f}°C"
        )


def display_stats(report):
    viz = TemperatureVisualizationService()
    viz.set_plot_style()

    st.subheader("Сезонная статистика")
    st.dataframe(report.seasonal_summary)
    st.write(f"Количество аномалий: {report.anomaly_count}")

    st.subheader("Визуализация данных")
    st.write("#### Временной ряд")
    st.pyplot(viz.draw_time_series(report.records, report.city_name))

    st.write("#### Boxplot по сезонам")
    st.pyplot(viz.draw_season_boxplot(report.records, report.city_name))

    st.write("#### Гистограмма температур")
    st.pyplot(viz.draw_temperature_histogram(report.records, report.city_name))

    st.write("#### Тепловая карта аномалий")
    st.pyplot(viz.draw_anomaly_heatmap(report.records, report.city_name))


if __name__ == "__main__":
    asyncio.run(main())
