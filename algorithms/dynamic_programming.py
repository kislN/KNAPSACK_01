import numpy as np

def dynamic_programming(capacity, weights, costs):

    n = len(weights)
    A = np.zeros((n + 1, capacity + 1), dtype=np.int)
    X = np.zeros((n + 1, capacity + 1), dtype=np.int)

    for i in range(n + 1):
        for w in range(capacity + 1):
            if i == 0 or w == 0:
                A[i, w] = 0
            elif (weights[i - 1] <= w) and (costs[i - 1] + A[i - 1, w - weights[i - 1]] > A[i - 1, w]):
                A[i, w] = costs[i - 1] + A[i - 1, w - weights[i - 1]]
                X[i, w] = 1
            else:
                A[i, w] = A[i - 1, w]

    items_ind = []
    cap = capacity

    for i in range(n, 0, -1):
        if X[i, cap] == 1:
            items_ind.append(i)
            cap -= weights[i - 1]

    items_ind.sort()
    items_ind = [x - 1 for x in items_ind]

    items = [0] * n

    for ind in items_ind:
        items[ind] = 1

    optimal_weight = (np.array(weights) * np.array(items)).sum()

    return A[n][capacity], optimal_weight, items






