import os
import shutil

import pyspark.sql.functions as F
from openlocationcode import openlocationcode

from python_code.config import *
from python_code.spark_utils import create_context


def convert_coordinate_to_grid(lat, long):
    try:
        return openlocationcode.encode(float(lat), float(long), 8)
    except:
        pass


def sample_data_and_write(df, output_path):
    df = df.limit(10000)
    output_path = os.path.abspath(output_path)
    return df.coalesce(1).write.csv(f'file://{output_path}', mode='overwrite', header=True)


def load_data(spark, input_path):
    input_path = os.path.abspath(input_path)
    df = spark.read.csv(input_path, header=True)
    return df


def add_grid_columns(df, columns_mapping=GRID_COLUMNS_MAPPING):
    convert_udf = F.udf(convert_coordinate_to_grid)
    for grid_column, lat_long_columns in columns_mapping.items():
        df = df.withColumn(grid_column, convert_udf(*lat_long_columns))
    return df


def find_most_used_grids(df, head=5, ):
    df = df.where(df[PICKUP_COLUMN] != df[DROPOFF_COLUMN])
    df = df.groupBy(PICKUP_COLUMN, DROPOFF_COLUMN).count().orderBy(F.desc('count'))
    df_head = df.head(head)
    return [(row[PICKUP_COLUMN], row[DROPOFF_COLUMN]) for row in df_head]


def write_pickup_dropoff_to_seperate_files(df, pickup_dropoff_pairs, result_path):
    result_path = os.path.abspath(result_path)
    for pickup, dropoff in pickup_dropoff_pairs:
        filtered = df.where(f'{PICKUP_COLUMN} = "{pickup}" and {DROPOFF_COLUMN} = "{dropoff}"')
        filtered.coalesce(1).write.csv(f'file://{result_path}/trip_data_{pickup}_{dropoff}',
                                       mode='overwrite', header=True)


def extract_csvs_from_output_subfolders(result_path):
    for subfolder in os.listdir(result_path):
        csv_temp_name = os.listdir(os.path.join(result_path, subfolder))
        csv_temp_name = [name for name in csv_temp_name if name.endswith('csv')][0]
        os.rename(os.path.join(result_path, subfolder, csv_temp_name),
                  os.path.join(result_path, f'{subfolder}.csv'))
        shutil.rmtree(os.path.join(result_path, subfolder), ignore_errors=True)


def extract_points_of_interest(spark):
    df = load_data(spark, TRIP_DATA_PATH)
    df = add_grid_columns(df)
    most_used = find_most_used_grids(df)
    return df, most_used


if __name__ == '__main__':
    spark = create_context(partitions=1000)
    df, most_used = extract_points_of_interest(spark)
    write_pickup_dropoff_to_seperate_files(df, most_used, TRIP_DATA_GRIDS_PATH)
    extract_csvs_from_output_subfolders(TRIP_DATA_GRIDS_PATH)
