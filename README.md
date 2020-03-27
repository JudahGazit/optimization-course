# optimization-course

Project Structure:
<pre>
├── README.md  // YOU ARE HERE
├── app.py // main python file: preparing the data, training the model, finding minimal values over random dates
├── optimization.pdf // the paper of this project
├── requirements.txt // standard python requirements file
├── experiment_results.csv // result of the experiment the python file is running
├── data
│   └── // contains the data necessary for running
├── latex
│   └── // contains the latex code creating the pdf file
└── python_code
   └── // contains the python code for this project
</pre>

Data taken from:
1. https://archive.org/details/nycTaxiTripData2013
2. https://www.kaggle.com/selfishgene/historical-hourly-weather-data
3. https://www.kaggle.com/gsnehaa21/federal-holidays-usa-19662020

The project contains a small sample of the original large dataset.
in order to recalculate the grid CSVs:
1. download data original separately (3.7 GB):
https://archive.org/download/nycTaxiTripData2013/trip_data.7z
2. Unzip to ./data/trip_data
3. Change the parameter `ENVIRONMENT = 'dev'` to `'prod'` in `python_code/config.py`

