import operator

def greedy_full_sort_infinity(knapsack_capacity, weights, items_cost):
  taken_count  = [0] * len(weights)
  actual_capacity = knapsack_capacity
  unit_costs  = dict(enumerate([items_cost[j] / weight for j, weight in enumerate(weights)]))
  sorted_unit_costs = dict(sorted(unit_costs.items(), key=operator.itemgetter(1),reverse=True))
  for index in sorted_unit_costs:
    if actual_capacity is 0:
      break
    taken_count[index] = int(actual_capacity / weights[index])
    actual_capacity -= (taken_count[index] * weights[index])
  return taken_count

def greedy_full_sort(knapsack_capacity, weights, items_cost):
  taken_count  = [0] * len(weights)
  actual_capacity = knapsack_capacity
  unit_costs  = dict(enumerate([items_cost[j] / weight for j, weight in enumerate(weights)]))
  sorted_unit_costs = dict(sorted(unit_costs.items(), key=operator.itemgetter(1),reverse=True))
  for index in sorted_unit_costs:
    if actual_capacity is 0:
      break
    possible_capacity = actual_capacity - weights[index]
    if possible_capacity > 0:
      taken_count[index] = 1
      actual_capacity = possible_capacity
  return taken_count
