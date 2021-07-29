import numpy as np
from copy import deepcopy


def iid_spw_function(state, server_win_probs):

    return server_win_probs[state["server"]]


def switch_servers(state):

    old_server, old_returner = state["server"], state["returner"]

    state["server"] = old_returner
    state["returner"] = old_server

    return state


def reset_points(state):

    state["points"] = {x: 0 for x in state["points"]}
    return state


def reset_games(state):

    state["games"] = {x: 0 for x in state["games"]}
    return state


def play_service_game(spw_function, state, has_ad=True):

    assert has_ad

    # State contains things like the current server
    server_win_prob = spw_function(state)

    server_points = state["points"][state["server"]]
    returner_points = state["points"][state["returner"]]

    if server_points >= 4 and (server_points - returner_points) >= 2:
        # Server wins
        state["games"][state["server"]] += 1
        return state["server"], state
    elif returner_points >= 4 and (returner_points - server_points) >= 2:
        state["games"][state["returner"]] += 1
        return state["returner"], state

    # Otherwise game is ongoing
    server_wins = np.random.uniform() < server_win_prob

    if server_wins:
        state["points"][state["server"]] += 1
    else:
        state["points"][state["returner"]] += 1

    return play_service_game(spw_function, state, has_ad=has_ad)


def play_tiebreak(spw_function, state):

    server_points = state["points"][state["server"]]
    returner_points = state["points"][state["returner"]]

    if server_points >= 7 and (server_points - returner_points) >= 2:
        # Server wins
        state["games"][state["server"]] += 1
        return state["server"], state
    elif returner_points >= 7 and (returner_points - server_points) >= 2:
        state["games"][state["returner"]] += 1
        return state["returner"], state

    # Otherwise game is ongoing
    if (server_points + returner_points) % 4 in [1, 3]:
        state = switch_servers(state)

    server_win_prob = spw_function(state)
    server_wins = np.random.uniform() < server_win_prob

    if server_wins:
        state["points"][state["server"]] += 1
    else:
        state["points"][state["returner"]] += 1

    return play_tiebreak(spw_function, state)


def play_set(spw_function, state, has_tiebreak=True, has_ad_games=True):

    assert has_tiebreak

    server_games = state["games"][state["server"]]
    returner_games = state["games"][state["returner"]]
    cur_server, cur_returner = state["server"], state["returner"]

    if server_games == 6 and returner_games == 6:

        tb_winner, state = play_tiebreak(spw_function, state)

        state["sets"][tb_winner] += 1

        state = reset_games(state)
        state = reset_points(state)

        # Switch servers from start of tiebreak
        state["server"] = cur_returner
        state["returner"] = cur_server

        return tb_winner, state

    elif server_games >= 6 and (server_games - returner_games) >= 2:

        # Server wins set
        state["sets"][cur_server] += 1

        state = reset_games(state)
        state = reset_points(state)

        return cur_server, state

    elif returner_games >= 6 and (returner_games - server_games) >= 2:

        # Returner wins set
        state["sets"][cur_returner] += 1

        state = reset_games(state)
        state = reset_points(state)

        return cur_returner, state

    else:

        # We're playing a normal service game
        game_winner, state = play_service_game(spw_function, state, has_ad=has_ad_games)
        state = reset_points(state)
        state = switch_servers(state)

        return play_set(
            spw_function, state, has_tiebreak=has_tiebreak, has_ad_games=has_ad_games
        )


def play_match(spw_function, state, best_of_three=True):

    cur_server, cur_returner = state["server"], state["returner"]
    server_sets = state["sets"][state["server"]]
    returner_sets = state["sets"][state["returner"]]

    target_sets = 2 if best_of_three else 3

    if server_sets == target_sets:
        return cur_server
    elif returner_sets == target_sets:
        return cur_returner
    else:
        set_winner, state = play_set(spw_function, state)
        return play_match(spw_function, state)
