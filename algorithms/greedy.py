import operator

def greedy_algorithm(capacity, weights, costs):

  n = len(weights)
  items  = [0] * n
  actual_capacity = capacity

  unit_costs  = dict(enumerate([costs[j] / weight for j, weight in enumerate(weights)]))
  sorted_unit_costs = dict(sorted(unit_costs.items(), key=operator.itemgetter(1), reverse=True))

  optimal_profit = 0
  optimal_weight = 0

  for index in sorted_unit_costs:
    if actual_capacity is 0:
      break
    possible_capacity = actual_capacity - weights[index]
    if possible_capacity > 0:
      items[index] = 1
      optimal_profit += costs[index]
      optimal_weight += weights[index]
      actual_capacity = possible_capacity

  return optimal_profit, optimal_weight, items
