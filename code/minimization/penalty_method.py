## time - time_of_day_max <= 0
## time_of_day_min - time <= 0

from code.minimization.nelder_mead import nelder_mead_minimize
from code.model.pretty_predict import predict


def penalty_predict(df, model, row, time_of_day, time_of_day_min, time_of_day_max, factor=1):
    res = predict(df, model, row, time_of_day)
    res += factor * max([time_of_day - time_of_day_max, 0]) ** 2
    res += factor * max([time_of_day_min - time_of_day, 0]) ** 2
    return res


def minimize_penalty_in_boundry(df, model, row, x0, xmin, xmax, factor_iterations, error=1e-5):
    print(f'minimize using {x0}, {xmin}, {xmax}, {factor_iterations}')
    res = None
    last_res = None
    counter = 0
    while (res is None or last_res is None or last_res[0] - res[0] > error) and counter < factor_iterations:
        last_res = res
        res_ = nelder_mead_minimize(lambda x: penalty_predict(df, model, row, x, xmin, xmax, 10 ** counter),
                                    [res[1] if res else x0])
        res_value = penalty_predict(df, model, row, res_, xmin, xmax, 10 ** counter)
        res = [res_value, res_[0], ]
        counter += 1
    return res


def minimize_penalty(df, model, row, x0, xmin, xmax, factor_iterations=5, boundry_iterations=10, error=1e-3):
    counter = 0
    min_res = minimize_penalty_in_boundry(df, model, row, x0, xmin, xmax, factor_iterations, error)
    min_left = None
    min_right = None
    while (min_left is None or min_right is None or max([min_res[0] - min_left[0], min_res[0] - min_right[0]]) > error) \
            and counter < boundry_iterations:
        min_res = min([min_res, min_left or [float('infinity')], min_right or [float('infinity')]])
        print(f'current minimum is {min_res[0], min_res[1] / 60 / 60}')
        min_left = minimize_penalty_in_boundry(df, model, row, xmin / 2, xmin, min_res[1], factor_iterations, error)
        min_right = minimize_penalty_in_boundry(df, model, row, xmax * 2, min_res[1], xmax, factor_iterations, error)
        counter += 1
    return min_res
