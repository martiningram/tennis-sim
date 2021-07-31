#!/usr/bin/python

from simulate import play_match
import numpy as np

def iid_spw_function(state):
    return 0.6 if state['server'] == 'A' else 0.5


def beta_spw_function(state):
    if state['server'] == 'A':
            return np.random.beta(0.6, 0.4, 1) # High-variance server
    else:
        return np.random.beta(0.6*20, 0.4*20, 1) # Equal low-variance server

n_runs = 10000
winners = []

for i in range(n_runs):
    state = {
        'server': 'A',
        'returner': 'B',
        'games': {'A': 0, 'B': 0},
        'points': {'A': 0, 'B': 0},
        'sets': {'A': 0, 'B': 0}
    }
    winners.append(play_match(spw_function=beta_spw_function, state=state))

np.savetxt('winners.csv', np.array(winners), delimiter=',', fmt='%s')
