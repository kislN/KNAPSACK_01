from scipy.optimize import linprog
import numpy as np


def bnb_recursive(capacity, weights, costs, bounds, low_bound=0, fixed_weight=0, ans=0):

    solve = linprog([-x for x in costs], [weights], [capacity], bounds=bounds, method='revised simplex')

    profit = - round(solve.fun, 6)
    X = [round(x, 6) for x in solve.x]

    if profit <= low_bound:
        return 0, 0



    flag = True
    for i, x in enumerate(X):
        if not x.is_integer():
            flag = False

            bounds[i] = [0, 0]
            new_profit, new_X = bnb_recursive(capacity, weights, costs, bounds, low_bound, fixed_weight, ans)
            if new_profit:
                low_bound = new_profit
                ans = new_X

            bounds[i] = [1, 1]
            fixed_weight += weights[i]
            if fixed_weight <= capacity:
                new_profit, new_X = bnb_recursive(capacity, weights, costs, bounds, low_bound, fixed_weight, ans)
                if new_profit:
                    low_bound = new_profit
                    ans = new_X

            bounds[i] = [0, 1]
            fixed_weight -= weights[i]

    if flag:
        low_bound = profit
        ans = X

    return low_bound, ans


def branch_and_bound(capacity, weights, costs):
    n = len(costs)
    bounds = [[0, 1]] * n
    optimal_profit, items = bnb_recursive(capacity, weights, costs, bounds)
    optimal_weight = (np.array(weights) * np.array(items)).sum()
    return int(optimal_profit), int(optimal_weight), list(np.array(items, dtype=np.int))
