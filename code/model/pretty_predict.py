import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from IPython.core.display import display


def plot_day_with_predict_func(df, model, predict):
    gen = df.sample(n=1, random_state=42)
    display(gen)
    gen = gen.values[0]
    x, y = [], []
    for i in range(0, 60 * 60 * 24, 100):
        x.append(i / 60 / 60)
        y.append(predict(df, model, gen, i))
    plt.plot(x, y)
    plt.savefig("mygraph.png")
    return gen


def predict(df, model, row, time_of_day=None, buffer=1000, buffer_samples=21):
    time_of_day_index = list(df.columns).index('time_of_day')
    rows = []
    time_of_day = time_of_day or row[time_of_day_index]
    for i in np.linspace(max(time_of_day - buffer, 0), min(time_of_day + buffer, 60 * 60 * 24), buffer_samples):
        row = row.copy()
        row[time_of_day_index] = i
        rows.append(row)
    rows = pd.DataFrame(rows, columns=df.columns)
    preds = model.predict(rows)
    return preds.mean()
