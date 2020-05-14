import time
import pandas as pd
import numpy as np

from algorithms.branch_and_bound import branch_and_bound as bnb
from algorithms.dynamic_programming import dynamic_programming as dynamic
from algorithms.greedy import greedy_algorithm as greedy
from algorithms.genetic import genetic_algorithm as genetic
from tools.time_limit import time_limit, TimeoutException


def get_time(knapsacks, methods=[dynamic, bnb, greedy, genetic], iters=3, lim_sec=10, file_name='time.csv'):
    df = pd.DataFrame(columns=['Method', "Knapsack's ID", 'Number of items', 'Mean', 'Median', 'Min', 'Max', 'Variance'])
    for i, knapsack in enumerate(knapsacks):
        for method in methods:
            time_list = []
            flag = 1
            for iter in range(0, iters):
                try:
                    with time_limit(lim_sec):
                        t0 = time.time()
                        method_ans = method(knapsack['capacity'], knapsack['weights'], knapsack['costs'])
                        t1 = time.time()
                        time_list.append(t1 - t0)

                except TimeoutException as e:
                    df = df.append(pd.Series([method.__name__, i, knapsack['n'], str(lim_sec) + ' seconds have passed!',
                                              np.nan, np.nan, np.nan, np.nan], index=df.columns), ignore_index=True)
                    flag = 0
                    break

            if flag:
                time_list = np.array(time_list)
                df = df.append(pd.Series([method.__name__, i, knapsack['n'], np.mean(time_list), np.median(time_list),
                                          np.min(time_list), np.max(time_list), np.var(time_list)],
                                         index=df.columns), ignore_index=True)

    df.to_csv('./data/output/' + file_name)
    return df


