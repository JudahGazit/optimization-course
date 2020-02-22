from IPython.core.display import display

from code.minimization.penalty_method import minimize_penalty
from code.model.model_learning import random_forest
from code.model.pretty_predict import plot_day_with_predict_func, predict

if __name__ == '__main__':
    df, model = random_forest()
    gen = plot_day_with_predict_func(df.drop(['trip_time_in_secs'], axis=1), model, predict=predict)
    # gen = df.drop(['trip_time_in_secs'], axis=1).sample(n=1, random_state=42)
    # display(gen)
    # gen = gen.values[0]
    res = minimize_penalty(df.drop(['trip_time_in_secs'], axis=1), model, gen, 6, 15 * 60 * 60, 17 * 60 * 60)
    display(res[0], res[1] / 60 / 60)
