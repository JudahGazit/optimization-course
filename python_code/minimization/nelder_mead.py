import numpy as np

ALPHA, GAMA, RO, SIGMA = 1., 2., 0.5, 0.5


def nelder_mead_terminate(iteration, iteration_limit, x, error=1e-3):
    if iteration >= iteration_limit:
        return True
    for i in range(len(x) - 1):
        if np.linalg.norm(x[i] - x[i + 1]) > error:
            return False
    return True


def nelder_mead_minimize_(f, n, xinit, iteration, error=1e-3, iteration_limit=100):
    xinit = sorted(xinit, key=f)
    fx = [f(x) for x in xinit]
    x0 = sum(xinit[:n]) / n
    if nelder_mead_terminate(iteration, iteration_limit, xinit, error):
        return x0
    else:
        xr = x0 + ALPHA * (x0 - xinit[n])
        if fx[0] <= f(xr) < fx[n]:
            return nelder_mead_minimize_(f, n, xinit[:n] + [xr], iteration + 1, error)
        if f(xr) < fx[0]:
            xe = x0 + GAMA * (xr - x0)
            if f(xe) < f(xr):
                return nelder_mead_minimize_(f, n, xinit[:n] + [xe], iteration + 1, error)
            else:
                return nelder_mead_minimize_(f, n, xinit[:n] + [xr], iteration + 1, error)
        else:
            xc = x0 + RO * (xinit[n] - x0)
            if f(xc) < fx[n]:
                return nelder_mead_minimize_(f, n, xinit[:n] + [xc], iteration + 1, error)
        shrink_xinit = [xinit[0]] + [xinit[0] + SIGMA * (x - xinit[0]) for x in xinit[1:]]
        return nelder_mead_minimize_(f, n, shrink_xinit, iteration + 1, error)


def nelder_mead_minimize(f, x0, error=1e-3, iteration_limit=100):
    x0 = np.array(list(x0))
    n = len(x0)
    xinit = [x0]
    for i in range(n):
        x = x0.copy()
        x[i] = float(x[i]) + 1
        xinit.append(x)
    return nelder_mead_minimize_(f, n, xinit, 0, error, iteration_limit)
