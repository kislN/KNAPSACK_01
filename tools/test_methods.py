import pandas as pd
import numpy as np
import time

from algorithms.branch_and_bound import branch_and_bound as bnb
from algorithms.dynamic_programming import dynamic_programming as dynamic
from algorithms.greedy import greedy_algorithm as greedy
from algorithms.genetic import genetic_algorithm as genetic
from tools.time_limit import time_limit, TimeoutException


def run_tests(knapsacks, methods=[dynamic, bnb, greedy, genetic], lim_sec=10, file_name='tests.csv'):

    df = pd.DataFrame(columns=['Method', "Knapsack's ID", 'Number of items', 'Optimal profit',
                               'Found profit', 'Found weight', 'Found X', 'Passed'])

    for method in methods:
        for i, knapsack in enumerate(knapsacks):
            answer = knapsack['optimal_profit']

            try:
                with time_limit(lim_sec):
                    method_ans = method(knapsack['capacity'], knapsack['weights'], knapsack['costs'])
                    profit = method_ans[0]
                    weight = method_ans[1]
                    X = method_ans[2]
                    df = df.append(pd.Series([method.__name__, i, knapsack['n'], answer, profit, weight,
                                              X, answer == profit], index=df.columns), ignore_index=True)
            except TimeoutException as e:
                df = df.append(pd.Series([method.__name__, i, knapsack['n'], answer, np.nan, np.nan, np.nan,
                                          str(lim_sec) + ' seconds have passed!'], index=df.columns), ignore_index=True)

    df.to_csv('./data/output/' + file_name)
    return df


def get_result(knapsack, knapsack_name, methods=[dynamic, bnb, greedy, genetic], iters=3, lim_sec=10, file_name='tests.csv'):

    df = pd.DataFrame(columns=["Knapsack", 'Method', 'Number of items', 'Mean time', 'Optimal profit',
                               'Found profit', 'Found weight', 'Found X', 'Passed'])


    for i, knapsack in enumerate(knapsack):
        for method in methods:
            answer = knapsack['optimal_profit']
            time_list = []
            flag = 1
            for iter in range(0, iters):
                try:
                    with time_limit(lim_sec):
                        t0 = time.time()
                        method_ans = method(knapsack['capacity'], knapsack['weights'], knapsack['costs'])
                        t1 = time.time()
                        time_list.append(t1 - t0)
                        profit = method_ans[0]
                        weight = method_ans[1]
                        X = method_ans[2]

                except TimeoutException as e:
                    df = df.append(pd.Series([knapsack_name, method.__name__, knapsack['n'], answer, np.nan, np.nan,
                                              np.nan, np.nan, str(lim_sec) + ' seconds have passed!'],
                                             index=df.columns), ignore_index=True)
                    flag = 0
                    break

            if flag:
                time_list = np.array(time_list)
                df = df.append(pd.Series([knapsack_name, method.__name__, knapsack['n'], np.mean(time_list), answer,
                                          profit, weight, X, answer == profit], index=df.columns), ignore_index=True)

    df.to_csv('./data/output/' + file_name)
    return df