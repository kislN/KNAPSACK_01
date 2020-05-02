def find_items_set(K, i, w, weights, items_set):
    if K[i][w] == 0:
        return

    if K[i - 1][w] == K[i][w]:
        find_items_set(K, i - 1, w, weights, items_set)
    else:
        find_items_set(K, i - 1, w - weights[i - 1], weights, items_set)
        items_set.append(i - 1)

    return items_set


def dynamic_programming(knapsack_capacity, weights, items_cost, with_items=True):
    n = len(weights)
    K = [[0 for x in range(knapsack_capacity + 1)] for x in range(n + 1)]

    for i in range(n + 1):
        for w in range(knapsack_capacity + 1):
            if i == 0 or w == 0:
                K[i][w] = 0
            elif weights[i - 1] <= w:
                K[i][w] = max(items_cost[i - 1] + K[i - 1][w - weights[i - 1]], K[i - 1][w])
            else:
                K[i][w] = K[i - 1][w]

    if with_items:
        items_set = []
        find_items_set(K, n, knapsack_capacity, weights, items_set)
        items = [0] * n
        for x in items_set:
            items[x] = 1
        return K[n][knapsack_capacity], items

    else:
        return K[n][knapsack_capacity]