def naive_minimize(f, xmin, xmax):
    results = []
    for x in range(xmin, xmax, 100):
        results.append([f(x), x])
    return min(results)
