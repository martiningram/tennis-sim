# How to use

To simulate matches, you can do the following:

```python
from simulate import play_match

n_runs = 10000
winners = list()

for i in range(n_runs):

    # Note it's important to make a fresh state each time as it is modified by
    # the function.
    state = {
        'server': 'A',
        'returner': 'B',
        'games': {'A': 0, 'B': 0},
        'points': {'A': 0, 'B': 0},
        'sets': {'A': 0, 'B': 0}
    }

    winners.append(play_match(spw_fun, state))
```

An important factor here is the `spw_fun`. For iid, you can do:

```python
def iid_spw_function(state):

    return 0.6 if state['server'] == 'A' else 0.5
```

For example. Basically, given a state, the function has to return a probability
for the server. You could also make this random:

```python
def random_spw_function(state):

    return np.random.uniform(low=0.5, high=0.6) if state['server'] == 'A' else
    np.random.uniform(low=0.6, high=0.7)
```

Hopefully this makes sense. Any function will do as long as it returns a win
probability.

So far, I have compared the simulations against some iid code, which is included
in the `winning_prob.py` file. You can see the comparisons in the `Compare
against iid.ipynb` notebook. It looks like things agree quite well, but if
anything looks amiss, please raise an issue / let me know.
