import pandas as pd

from python_code.config import PATH


def load_weather_file(file_name):
    weather = pd.read_csv(PATH + f'weather/{file_name}.csv')
    weather = weather[['datetime', 'New York']]
    weather.columns = ['datetime', file_name]
    return weather


def add_weather(df):
    df = df.copy()
    weather_files = ['humidity', 'pressure', 'temperature', 'weather_description', 'wind_direction', 'wind_speed']
    df['datetime'] = df.pickup_datetime.dt.strftime('%Y-%m-%d %H:00:00')
    for file in weather_files:
        weather = load_weather_file(file)
        df = df.merge(weather, on=['datetime'])
    df = df.drop(['datetime'], axis=1)
    return df
