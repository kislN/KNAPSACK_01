from scipy.optimize import linprog


def bnb_recursive(capacity, weights, costs, n, bounds, low_bound=0, ans=0):
    solve = linprog([-x for x in costs], [weights], [capacity], bounds=bounds)

    fun = - round(solve.fun, 6)
    X = [round(x, 6) for x in solve.x]

    if fun <= low_bound:
        return 0, 0

    flag = True

    for i, x in enumerate(X):
        if not x.is_integer():
            flag = False

            bounds[i] = [0, 0]
            new_fun, new_X = bnb_recursive(capacity, weights, costs, n, bounds, low_bound, ans)
            if new_fun:
                low_bound = new_fun
                ans = new_X

            bounds[i] = [1, 1]
            new_fun, new_X = bnb_recursive(capacity, weights, costs, n, bounds, low_bound, ans)
            if new_fun:
                low_bound = new_fun
                ans = new_X

            bounds[i] = [0, 1]

    if flag:
        low_bound = fun
        ans = X

    return low_bound, ans


def branch_and_bound(capacity, weights, costs):
    n = len(costs)
    bounds = [[0, 1]] * n
    fun, x = bnb_recursive(capacity, weights, costs, n, bounds)
    return fun, x
