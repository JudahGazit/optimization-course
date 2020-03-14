def binary_minimize(f, xmin, xmax, error=1e-3):
    b = (xmax + xmin) / 2
    if xmax - xmin > error:
        b_left = (b + xmin) / 2
        b_right = (xmax + b) / 2
        if f(b_left) < f(b_right):
            return binary_minimize(f, xmin, b)
        else:
            return binary_minimize(f, b, xmax)
    return [f(b), b]
