# optimization-course

Project Structure:





The project contains a small sample of the original large dataset.

in order to recalculate the grid CSVs:
1. download data original separately (3.7 GB):
https://archive.org/download/nycTaxiTripData2013/trip_data.7z
2. Unzip to ./data/trip_data
3. Change the parameter `ENVIRONMENT = 'dev'` to `'prod'` in `python_code/config.py`