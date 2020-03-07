from IPython.core.display import display

from python_code.minimization.penalty_method import minimize_penalty
from python_code.model.data_prep import data_prep
from python_code.model.model_learning import random_forest
from python_code.model.pretty_predict import plot_day_with_predict_func, predict

if __name__ == '__main__':
    df = data_prep()
    df, model = random_forest(df)
    gen = plot_day_with_predict_func(df.drop(['trip_time_in_secs'], axis=1), model, predict=predict)
    res = minimize_penalty(df.drop(['trip_time_in_secs'], axis=1), model, gen, 6, 11 * 60 * 60, 12 * 60 * 60)
    display(res[0], res[1] / 60 / 60)
