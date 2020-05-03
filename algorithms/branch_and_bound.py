from scipy.optimize import linprog
import numpy as np
import operator


def bnb_recursive(capacity, weights, costs, bounds, low_bound=0, fixed_weight=0, ans=0):

    solve = linprog([-x for x in costs], [weights], [capacity], bounds=bounds, method='revised simplex')

    profit = - round(solve.fun, 6)
    X = [round(x, 6) for x in solve.x]

    if profit <= low_bound:
        return 0, 0

    inds_dict = dict(enumerate(round(abs(x - 0.5), 4) for x in X))
    inds_dict = {key: val for key, val in inds_dict.items() if val != 0.5}
    inds_dict = dict(sorted(inds_dict.items(), key=operator.itemgetter(1), reverse=True))

    if len(inds_dict):

        i = list(inds_dict.keys())[0]

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

    else:
        low_bound = profit
        ans = X

    return low_bound, ans


def branch_and_bound(capacity, weights, costs):
    print('hey')
    n = len(costs)
    bounds = [[0, 1]] * n
    optimal_profit, items = bnb_recursive(capacity, weights, costs, bounds)
    optimal_weight = (np.array(weights) * np.array(items)).sum()
    return int(optimal_profit), int(optimal_weight), list(np.array(items, dtype=np.int))
