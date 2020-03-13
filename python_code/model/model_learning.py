import pandas as pd
from IPython.core.display import display
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import *


def l1_diff(x, y):
    return abs((x - y))


def print_score(m, x_train, y_train, x_test, y_test):
    rows = []
    rows.append(['l1 - mean', l1_diff(m.predict(x_train), y_train).mean(), l1_diff(m.predict(x_test), y_test).mean()])
    rows.append(['l1 - std', l1_diff(m.predict(x_train), y_train).std(), l1_diff(m.predict(x_test), y_test).std()])
    rows.append(['l1 - quantile', l1_diff(m.predict(x_train), y_train).quantile(),
                 l1_diff(m.predict(x_test), y_test).quantile()])
    rows.append(['l1 - 95% percentile', l1_diff(m.predict(x_train), y_train).quantile(0.95),
                 l1_diff(m.predict(x_test), y_test).quantile(0.95)])
    rows.append(['l1 - min', l1_diff(m.predict(x_train), y_train).min(), l1_diff(m.predict(x_test), y_test).min()])
    rows.append(['l1 - max', l1_diff(m.predict(x_train), y_train).max(), l1_diff(m.predict(x_test), y_test).max()])
    rows.append(['r2', m.score(x_train, y_train), m.score(x_test, y_test)])
    rows.append(['r2 - oob', m.oob_score_, None])
    df = pd.DataFrame(rows, columns=['name', 'train', 'test'])
    display(df)


def random_forest(df):
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)
    x_train, y_train = train_df.drop('trip_time_in_secs', axis=1), train_df.trip_time_in_secs
    x_test, y_test = test_df.drop('trip_time_in_secs', axis=1), test_df.trip_time_in_secs
    m = RandomForestRegressor(n_jobs=-1, n_estimators=40, max_features=0.9, min_samples_leaf=3, oob_score=True)
    m.fit(x_train, y_train)
    print_score(m, x_train, y_train, x_test, y_test)
    return df, m
