import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from cachey import Cache


def plot_day_with_predict_func(regressor):
    x, y = [], []
    for i in range(0, 60 * 60 * 24, 100):
        x.append(i / 60 / 60)
        y.append(regressor(i))
    plot(x, y)


def plot(x, y):
    fig = plt.figure()
    ax = fig.gca()
    ax.set_xticks(np.arange(0, 24, 1))
    ax.set_xlabel('Start Time (hours)')
    ax.set_ylabel('Travel Time (seconds)')
    ax.set_title('Travel Time During the Day')
    plt.plot(x, y)
    plt.grid()
    plt.savefig("mygraph.png")


def predict(model, row, time_of_day=None, buffer=1000, buffer_samples=21):
    rows = []
    time_of_day = time_of_day or row['time_of_day']
    for i in np.linspace(max(time_of_day - buffer, 0), min(time_of_day + buffer, 60 * 60 * 24), buffer_samples):
        row = row.copy()
        row['time_of_day'] = i
        rows.append(row)
    preds = model.predict(pd.DataFrame(rows))
    return preds.mean()


def model_predict(model, row, time_of_day=None):
    row['time_of_day'] = time_of_day or row.get('time_of_day')
    pred = model.predict(pd.DataFrame([row]))
    return pred[0]


def get_regressor(model, x, predict):
    return lambda t: predict(model, x, t)


c = Cache(1e9)
predict = c.memoize(predict)
