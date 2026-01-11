from typing import Tuple, Optional, Dict
from io import StringIO
from pathlib import Path
import pandas as pd
import aiofiles
import time
from multiprocessing import Pool

def validate_dataframe(df: pd.DataFrame) -> Tuple[bool, str, Optional[pd.DataFrame]]:
    required_cols = {'city', 'timestamp', 'temperature', 'season'}
    if not required_cols.issubset(df.columns):
        missing = required_cols - set(df.columns)
        return False, f"Отсутствуют колонки: {missing}", None
    df_copy = df.copy()
    df_copy['timestamp'] = pd.to_datetime(df_copy['timestamp'])
    if not pd.api.types.is_numeric_dtype(df_copy['temperature']):
        return False, "Колонка 'temperature' должна быть числовой", None
    return True, "Данные валидны", df_copy

async def read_csv_async(file) -> Tuple[bool, str, Optional[pd.DataFrame]]:
    try:
        if isinstance(file, (str, Path)):
            async with aiofiles.open(file, 'r') as f:
                content = await f.read()
        else:
            content = file.getvalue().decode()
        df = pd.read_csv(StringIO(content))
        return validate_dataframe(df)
    except Exception as e:
        return False, f"Ошибка при загрузке CSV: {e}", None

def _analyze_city(df: pd.DataFrame, city: str) -> Dict:
    city_df = df[df['city'] == city].copy()
    city_df['rolling_avg'] = city_df['temperature'].rolling(window=30, center=True).mean()
    seasonal_stats = city_df.groupby('season').agg({'temperature': ['mean', 'std']}).round(2)
    city_df['is_anomaly'] = False
    for s in seasonal_stats.index:
        mask = city_df['season'] == s
        stats = seasonal_stats.loc[s]
        city_df.loc[mask, 'is_anomaly'] = ((city_df.loc[mask, 'temperature'] > stats[('temperature','mean')] + 2*stats[('temperature','std')]) |
                                           (city_df.loc[mask, 'temperature'] < stats[('temperature','mean')] - 2*stats[('temperature','std')]))
    return {'city': city, 'seasonal_stats': seasonal_stats, 'data': city_df}

def _process_city_for_pool(df_dict, city):
    import pandas as pd
    return _analyze_city(pd.DataFrame(df_dict), city)

def run_parallel_analysis(df: pd.DataFrame) -> Tuple[Dict, float]:
    cities = df['city'].unique()
    df_dict = df.to_dict('list')
    start = time.time()
    # with Pool() as pool:
    #     results = pool.starmap(lambda d, c: _analyze_city(pd.DataFrame(d), c), [(df_dict, c) for c in cities])
    with Pool() as pool:
        results = pool.starmap(
            _process_city_for_pool,
            [(df_dict, c) for c in cities]
        )
    return {r['city']: r for r in results}, time.time()-start
