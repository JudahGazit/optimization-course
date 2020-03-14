# optimization-course

Project Structure:

├── README.md  // YOU ARE HERE<br>
├── app.py // main python file: preparing the data, training the model, finding minimal values over random dates<br>
├── optimization-paper.pdf // the paper of this project<br>
├── requirements.txt // standard python requirements file<br>
├── experiment_results.csv // result of the experiment the python file is running<br>
├── data <br>
│   └── // contains the data necessary for running <br>
├── latex <br>
│   ├── // contains the latex code creating the pdf file <br>
├── python_code <br>
│   ├── // contains the python code for this project <br>


The project contains a small sample of the original large dataset.
in order to recalculate the grid CSVs:
1. download data original separately (3.7 GB):
https://archive.org/download/nycTaxiTripData2013/trip_data.7z
2. Unzip to ./data/trip_data
3. Change the parameter `ENVIRONMENT = 'dev'` to `'prod'` in `python_code/config.py`