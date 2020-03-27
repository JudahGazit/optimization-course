## time - time_of_day_max <= 0
## time_of_day_min - time <= 0


def penalty_predict(regressor, time_of_day, time_of_day_min, time_of_day_max, factor=1):
    res = regressor(time_of_day)
    res += factor * max([time_of_day - time_of_day_max, 0]) ** 2
    res += factor * max([time_of_day_min - time_of_day, 0]) ** 2
    return res


def get_penalty_wrapper(regressor, time_of_day_min, time_of_day_max):
    return lambda t, factor: penalty_predict(regressor, t, time_of_day_min, time_of_day_max, factor)


def minimize_penalty_in_boundry(regressor, t0, tmin, tmax, factor_iterations, minimizer, error=1e-5):
    print(f'minimize using {t0}, {tmin}, {tmax}, {factor_iterations}')
    res = None
    last_res = None
    counter = 0
    penalty = get_penalty_wrapper(regressor, tmin, tmax)
    while (res is None or last_res is None or last_res[0] - res[0] > error) and counter < factor_iterations:
        last_res = res
        res_ = minimizer(f=lambda t: penalty(t, 10 ** counter), x0=[res[1] if res else t0])
        res_value = penalty(res_, 10 ** counter)
        res = [res_value, res_[0]]
        counter += 1
    res = min([res, [regressor(tmin), tmin], [regressor(tmax), tmax]])
    return res
