import pandas as pd

from code.config import PATH


def add_weather(df):
    df = df.copy()
    weather = pd.read_csv(PATH + 'nyc-weather.csv')
    weather = weather[weather.NAME == 'NY CITY CENTRAL PARK, NY US'][
        ['DATE', 'TMAX', 'TMIN', 'PRCP', 'SNOW', 'SNWD', 'AWND', 'WDF2', 'WDF5', 'WSF2', 'WSF5']]
    weather.TMAX = (weather.TMAX - 32) * 5.0 / 9.0
    weather.TMIN = (weather.TMIN - 32) * 5.0 / 9.0
    df = df.merge(weather, on=['DATE'], )
    return df
