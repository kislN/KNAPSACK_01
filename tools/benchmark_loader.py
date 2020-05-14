import requests
import numpy as np
from os.path import join
import os

def get_knapsack(n='01') -> dict:

    bas_url = 'https://people.sc.fsu.edu/~jburkardt/datasets/knapsack_01/p'

    c  = requests.get(bas_url+n+'_c.txt')
    w  = requests.get(bas_url+n+'_w.txt')
    p  = requests.get(bas_url+n+'_p.txt')
    s  = requests.get(bas_url+n+'_s.txt')

    kdct = {'capacity': c.text,
            'weights':  w.text,
            'costs':    p.text,
            'optimal':  s.text,

            }

    kdct = {k: v.split('\n') for k, v in kdct.items()}
    kdct = {k: [int(x) for x in v if len(x) > 0] for k, v in kdct.items()}

    kdct['capacity'] = kdct['capacity'][0]
    kdct['n'] = len(kdct['weights'])
    kdct['optimal_profit'] = (np.array(kdct['costs']) * np.array(kdct['optimal'])).sum()

    print('P' + n, 'is loaded!')
    kdct['name'] = 'P_' + n

    return kdct

def get_one_more_knapsack(direct='large_scale', file_name='knapPI_1_100_1000_1') -> dict:

    kdct = {}
    path = './data/instances_01_KP'

    with open(join(path, direct, file_name), 'r') as f:
        file = f.read()
        file = file.split('\n')

        kdct['n']        = int(file[0].split(' ')[0])
        kdct['capacity'] = int(file[0].split(' ')[1])
        kdct['weights']  = [int(x.split(' ')[1]) for x in file[1:kdct['n']+1]]
        kdct['costs']    = [int(x.split(' ')[0]) for x in file[1:kdct['n']+1]]

    with open(join(path, direct + '-optimum', file_name), 'r') as f:
        file = f.read()
        file = file.split('\n')
        kdct['optimal_profit'] = int(file[0])

    kdct['name'] = file_name
    print(file_name + ' is loaded!')

    return kdct


def get_all_knapsacks() -> list:

    path = './data/instances_01_KP'
    dir_large = 'large_scale'
    dir_small = 'low-dimensional'

    knapsacks = []

    for i in range(1, 8):
        knapsacks.append(get_knapsack('0' + str(i)))

    for file_name in os.listdir(join(path, dir_small)):
        knapsacks.append(get_one_more_knapsack(dir_small, file_name))

    for file_name in os.listdir(join(path, dir_large)):
        knapsacks.append(get_one_more_knapsack(dir_large, file_name))

    knapsacks = sorted(knapsacks, key=lambda x: x['n'])
    knapsacks

    return knapsacks

