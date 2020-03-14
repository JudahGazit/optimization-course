import pandas as pd
from IPython.core.display import display

from python_code.minimization.naive_minimum import naive_minimize
from python_code.minimization.nelder_mead import nelder_mead_minimize
from python_code.minimization.penalty_method import minimize_penalty_in_boundry
from python_code.model.data_prep import data_prep
from python_code.model.model_learning import random_forest
from python_code.model.pretty_predict import plot_day_with_predict_func, predict, get_regressor


def experiment(df, model):
    states = range(1, 10)
    logs = []
    for state in states:
        row = df.sample(n=1, random_state=state).drop('trip_time_in_secs', 1).to_dict('records')[0]
        regressor = get_regressor(model, row, predict)
        res1 = minimize_penalty_in_boundry(regressor, 0, 10 * 60 * 60, 12 * 60 * 60, 10, nelder_mead_minimize)
        res2 = minimize_penalty_in_boundry(regressor, 13 * 60 * 60, 10 * 60 * 60, 12 * 60 * 60, 10,
                                           nelder_mead_minimize)
        res3 = naive_minimize(regressor, 10 * 60 * 60, 12 * 60 * 60)
        log = {'date': f'{row["pickup_datetimeday"]} / {row["pickup_datetimemonth"]}',
               'nelder_mead_0_predict': res1[0], 'nelder_mead_0_starttime': res1[1] / 60 / 60,
               'nelder_mead_13_predict': res2[0], 'nelder_mead_13_starttime': res2[1] / 60 / 60,
               'naive_method_predict': res3[0], 'naive_method_starttime': res3[1] / 60 / 60,
               }
        logs.append(log)
        display(log)
    return logs


if __name__ == '__main__':
    df = data_prep()
    df, model = random_forest(df)
    row = df.sample(n=1, random_state=49).drop('trip_time_in_secs', 1).to_dict('records')[0]
    regressor = get_regressor(model, row, predict)
    plot_day_with_predict_func(regressor)
    res = minimize_penalty_in_boundry(regressor, 13 * 60 * 60, 10 * 60 * 60, 12 * 60 * 60, 10, nelder_mead_minimize)
    display(res[0], res[1] / 60 / 60)
    logs = experiment(df, model)
    pd.DataFrame(logs).to_csv('experiment_results.csv', header=True)
