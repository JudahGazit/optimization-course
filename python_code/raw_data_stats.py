import os

import matplotlib.pyplot as plt
import pandas as pd

from python_code.config import TRIP_DATA_GRIDS_PATH


def load_data(pickup_grid='87G8Q279+', dropoff_grid='87G8Q225+'):
    data_path = os.path.join(os.path.abspath(TRIP_DATA_GRIDS_PATH), f'trip_data_{pickup_grid}_{dropoff_grid}.csv')
    df = pd.read_csv(data_path)
    df = df[(df.trip_time_in_secs > 0) & (df.trip_distance > 0.05) & (df.trip_distance < 2)]
    return df


def trip_time_hist(df):
    axs = plt.subplot()
    axs.set_xlabel('Trip time in seconds')
    axs.set_ylabel('Amount')
    axs.set_title('Trip time (in seconds) Histogram')
    h = axs.hist(df.trip_time_in_secs, bins=100, )
    return axs


def time_of_day_hist(df):
    df = df.copy()
    df['time_of_day'] = pd.to_datetime(df.pickup_datetime).apply(
        lambda d: d.hour * 60 * 60 + d.minute * 60 + d.second)
    axs = plt.subplot()
    axs.set_xlabel('Time since 00:00 in seconds')
    axs.set_ylabel('Amount')
    axs.set_title('Time of Day (in seconds) Histogram')
    h = axs.hist(df.time_of_day, bins=100, )
    return axs


def trip_speed_hist(df):
    axs = plt.subplot()
    axs.set_xlabel('Trip distance / trip time in seconds')
    axs.set_ylabel('Amount')
    axs.set_title('Trip Speed (Miles / second) Histogram')
    h = axs.hist(df.trip_distance / df.trip_time_in_secs, bins=100, )
    return axs


def trip_distance_hist(df):
    axs = plt.subplot()
    axs.set_xlabel('Trip distance in miles')
    axs.set_ylabel('Amount')
    axs.set_title('Trip Distance Histogram')
    h = axs.hist(df.trip_distance, bins=100, )


def run_and_save_png(png_path, func, *args, **kwargs):
    graph = func(*args, **kwargs)
    plt.savefig(os.path.join(png_output_path, func.__name__ + '.png'))
    plt.clf()


if __name__ == '__main__':
    df = load_data()
    graphs = [trip_time_hist, time_of_day_hist, trip_speed_hist, trip_distance_hist]
    png_output_path = os.path.abspath('./latex')
    for graph in graphs:
        run_and_save_png(png_output_path, graph, df)
