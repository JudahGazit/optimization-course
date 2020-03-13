import numpy as np
import pandas as pd

from python_code.config import PATH


def load_weather_file(file_name):
    weather = pd.read_csv(PATH + f'weather/{file_name}.csv')
    weather = weather[['datetime', 'New York']]
    weather.columns = ['datetime', file_name]
    weather.datetime = pd.to_datetime(weather.datetime, utc=True)
    weather.datetime = weather.datetime.dt.tz_convert('US/Eastern')
    weather.datetime = weather.datetime.dt.strftime('%Y-%m-%d 00:00:00')
    weather = calculate_daily_mean(weather, file_name)
    return weather


def calculate_daily_mean(weather_dataset, file_name, date_column='datetime'):
    if weather_dataset.dtypes[file_name] == np.float:
        mean_column, min_column, max_column = f'{file_name}_daily_mean', f'{file_name}_daily_min', f'{file_name}_daily_max'
        means = weather_dataset[[date_column, file_name]]
        means[mean_column] = means[file_name]
        means[min_column] = means[file_name]
        means[max_column] = means[file_name]
        means = means.groupby([date_column], as_index=False).agg(
            {mean_column: 'mean', min_column: 'min', max_column: 'max'})
        means = means[[date_column, mean_column, min_column, max_column]]
        weather_dataset = means
    return weather_dataset


def add_weather(df):
    df = df.copy()
    weather_files = ['humidity', 'pressure', 'temperature', 'wind_direction', 'wind_speed']
    df['datetime'] = df.pickup_datetime.dt.strftime('%Y-%m-%d 00:00:00')
    for file in weather_files:
        weather = load_weather_file(file)
        df = df.merge(weather, on=['datetime'])
    df = df.drop(['datetime'], axis=1)
    return df
