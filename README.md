# python_hw1# Мониторинг и анализ температур

Приложение для анализа исторических температурных данных и отслеживания текущей температуры через OpenWeatherMap API.

## Возможности

- Загрузка исторических данных о температуре
- Выявление аномальных значений
- Визуализация температурных трендов по городам
- Отслеживание текущей температуры и сравнение с историей
- Поддержка веб-интерфейса и консольного запуска

## Структура проекта
```sh
├── LICENSE                              # лицензия
├── README.md                            # описание проекта
├── requirements.txt                     # зависимости
├── streamlit_app.py                     # веб-приложение
├── main.py                              # консольное приложение
├── data                                 # директория с данными
│   └── temperature_data.csv             # пример данных
├── logs                                 # папка для логов
│   ├── app.log                          # лог веб-приложения
│   └── errors.log                       # лог ошибок
├── notebooks                            # ноутбуки
│   └── data_analysis.ipynb              # анализ данных
├── src                                  # исходный код
│   ├── config.py                        # конфигурация проекта
│   ├── core                             # базовые компоненты
│   │   ├── logger.py                    # инициализация логгера
│   │   └── log_config.py                # настройки логирования
│   ├── services                         # сервисы
│   │   ├── temperature_analysis_service.py
│   │   ├── city_weather_service.py
│   │   └── visualization_service.py
│   └── utils                            # вспомогательные функции
│       └── data_utils.py                   
```
## Установка

1. Клонируйте репозиторий:

```bash
git clone https://github.com/psaw/python-hw1.git temperature-analysis
cd temperature-analysis
```

2. Создайте виртуальное окружение и активируйте его:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/MacOS
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте файл `.env` в корневой директории и добавьте API ключ:
```
OPENWEATHER_API_KEY=ваш_ключ
```

## Запуск

### Веб-интерфейс

Запустите Streamlit приложение:
```bash
streamlit run streamlit_app.py
```

Приложение будет доступно по адресу: http://localhost:8501

### Консольное приложение

Для анализа данных через командную строку:
```bash
python main.py
```

## Основные компоненты

### TemperatureAnalysisService
Сервис для анализа температурных данных:
- Расчет скользящего среднего
- Сезонная статистика
- Определение аномалий

### CityWeatherFetcher

- Получение текущей температуры
- Проверка на аномалии
- Кэширование результатов

### TemperatureVisualizationService

- Временные ряды температур
- Boxplot по сезонам
- Гистограммы
- Тепловые карты аномалий

## Требования

- Python 3.12
- pandas
- matplotlib
- seaborn
- streamlit
- aiohttp
- aiofiles
- python-dotenv
- loguru

