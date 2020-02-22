PATH = './data/'

TRIP_DATA_PATH = PATH + 'trip_data'
TRIP_DATA_GRIDS_PATH = PATH + 'trip_data_grids'

PICKUP_COLUMN = 'pickup_grid'
DROPOFF_COLUMN = 'dropoff_grid'

GRID_COLUMNS_MAPPING = {
    PICKUP_COLUMN: ['pickup_latitude', 'pickup_longitude'],
    DROPOFF_COLUMN: ['dropoff_latitude', 'dropoff_longitude']
}
