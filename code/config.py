ENVIRONMENT = 'dev'  ## change to prod to full data processing
PATH = './data/'

TRIP_DATA_PATH = PATH + 'trip_data/trip_data_1.csv'
TRIP_DATA_SAMPLE_PATH = PATH + 'trip_data_sample'
TRIP_DATA_GRIDS_PATH = PATH + 'trip_data_grids'

if ENVIRONMENT != 'prod':
    TRIP_DATA_PATH = TRIP_DATA_SAMPLE_PATH

PICKUP_COLUMN = 'pickup_grid'
DROPOFF_COLUMN = 'dropoff_grid'

GRID_COLUMNS_MAPPING = {
    PICKUP_COLUMN: ['pickup_latitude', 'pickup_longitude'],
    DROPOFF_COLUMN: ['dropoff_latitude', 'dropoff_longitude']
}
