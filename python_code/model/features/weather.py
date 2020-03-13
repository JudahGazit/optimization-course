import numpy as np
import pandas as pd

from python_code.config import PATH


def load_weather_file(file_name):
    weather = pd.read_csv(PATH + f'weather/{file_name}.csv')
    weather = weather[['datetime', 'New York']]
    weather.columns = ['datetime', file_name]
    weather.datetime = pd.to_datetime(weather.datetime, utc=True)
    weather.datetime = weather.datetime.dt.tz_convert('US/Eastern')
    weather = calculate_daily_mean(weather, file_name)
    weather.datetime = weather.datetime.dt.strftime('%Y-%m-%d %H:00:00')
    return weather


def calculate_daily_mean(weather_dataset, file_name, date_column='DATE'):
    if weather_dataset.dtypes[file_name] == np.float:
        weather_dataset[date_column] = weather_dataset.datetime.dt.strftime('%Y-%m-%d')
        mean_column, min_column, max_column = f'{file_name}_daily_mean', f'{file_name}_daily_min', f'{file_name}_daily_max'
        means = weather_dataset[[date_column, file_name]]
        means[mean_column] = means[file_name]
        means[min_column] = means[file_name]
        means[max_column] = means[file_name]
        means = means.groupby([date_column], as_index=False).agg(
            {mean_column: 'mean', min_column: 'min', max_column: 'max'})
        means = means[[date_column, mean_column, min_column, max_column]]
        weather_dataset = weather_dataset.merge(means, on=[date_column]).drop([date_column], 1)
    return weather_dataset


def add_weather(df):
    df = df.copy()
    weather_files = ['humidity', 'pressure', 'temperature', 'weather_description', 'wind_direction', 'wind_speed']
    df['datetime'] = df.pickup_datetime.dt.strftime('%Y-%m-%d %H:00:00')
    for file in weather_files:
        weather = load_weather_file(file)
        df = df.merge(weather, on=['datetime'])
    df = df.drop(['datetime'], axis=1)
    return df
