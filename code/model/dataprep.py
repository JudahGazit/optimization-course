import os

import numpy as np
import pandas as pd

from code.config import TRIP_DATA_GRIDS_PATH
from code.model.features.date_parts import add_date_parts
from code.model.features.holidays import add_holidays
from code.model.features.weather import add_weather

features = [add_holidays, add_weather, add_date_parts]


def format_dates(df):
    df = df.copy()
    df.pickup_datetime = pd.to_datetime(df.pickup_datetime, format='%Y-%m-%d %H:%M:%S')
    df['time_of_day'] = df.pickup_datetime.apply(lambda d: d.timestamp() % (24 * 60 * 60))
    df['DATE'] = df.pickup_datetime.dt.strftime('%Y-%m-%d')
    return df


def load_data(pickup_grid='87G8Q279+', dropoff_grid='87G8Q225+',
              select_cols=['pickup_datetime', 'trip_time_in_secs', 'trip_distance']):
    data_path = os.path.join(os.path.abspath(TRIP_DATA_GRIDS_PATH), f'trip_data_{pickup_grid}_{dropoff_grid}.csv')
    df_grid = pd.read_csv(data_path)
    df_grid = df_grid[select_cols]
    df_grid = format_dates(df_grid)
    return df_grid


def remove_nulls_from_columns(df):
    df = df.copy()
    df = df.drop(['pickup_datetime', 'DATE'], axis=1)
    df.WSF5 = df.WSF5.apply(lambda x: 0 if np.isnan(x) else x)
    df.WDF5 = df.WDF5.apply(lambda x: 0 if np.isnan(x) else x)
    return df


def apply_features(base_df, features=features):
    df = base_df.copy()
    for feature in features:
        df = feature(df)
    df = df.sort_values('pickup_datetime')
    return df


def clean_anomalies(df):
    df.copy()
    df = df[(df.trip_distance > 0.05) & (df.trip_distance <= 2)]
    return df


def dataprep():
    df = load_data()
    df = apply_features(df)
    df = clean_anomalies(df)
    df = remove_nulls_from_columns(df)
    return df
