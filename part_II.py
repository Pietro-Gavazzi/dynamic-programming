"""
LINFO_2275: Data mining and Decision making
Project Part II: Two players

authors: Pietro GAVAZZI, Francis JACOBS, Alex WLODAWER
"""


import numpy as np
from part_I import value_iteration, expected_new_places



# %%     


# Computes the expected probability of winning for the current player based on the given state and action.
def expected_probability_win(state, action, P, layout, circle, nb_turn, nb_turn_solo):
    # state = (position1:(), positions2:(), whoseturn)
    # nb_turn = (tour joueur whoseturn, tour joueur autre)
    # probabilité de gagner du joueur 1
    # if whoseturn==1:-> max
    # if whoseturn==2:-> min


    def switch_player(whoseturn):
        # if whoseturn is 1 return 2, if whoseturn is 2 return 1
        return (whoseturn-1)*1 + (2-whoseturn)*2
    

    (my_place, other_place, whoseturn) = state

    # If other_player is in position 14, that means that other_player won 
    # Thus if it is the turn of player 2, we return 1 because player 1 wins with probability 1, and if it is the turn of player 1 we return 0
    # The number of turns that the current player is expected to take to reach the position 14 is thus equal to the number of turns when he plays alone from his place,
    # the other player is already in position 14 so he takes 0 turns
    if other_place[0] == 14:
        if whoseturn==2: return 1, np.array([nb_turn_solo[my_place], 0.])
        else: return 0, np.array([nb_turn_solo[my_place], 0.])
    
    # we calculate the expected new place of the playere whose turn is 
    list_expected_my_new_places = expected_new_places(my_place, action, layout, circle)


    new_probability  = 0
    new_nb_turn = np.array([1., 0.])
    
    for (p_my_new_place, my_new_place) in list_expected_my_new_places:

        new_probability += p_my_new_place*P[(other_place, my_new_place, switch_player(whoseturn))] 

        nb_turn_next_state = nb_turn[(other_place, my_new_place, switch_player(whoseturn))]
        new_nb_turn +=p_my_new_place*np.array([nb_turn_next_state[1], nb_turn_next_state[0]])

    return new_probability, new_nb_turn

    

# this function calculates the [probability of win of player 1] (which is equal to 1-[probability of win of the player 2])
def min_max(layout, circle, n):

    # we define the different states as follows:
    # (my_place, other_place, whoseturn) = state
    possible_places = []
    for i in range(14):
        if layout[i]>=3:
            possible_places.append((i, False))
            possible_places.append((i, True))
        else:
            possible_places.append((i, False))

    possible_states = []
    for place1 in possible_places:
        for place2 in possible_places:
            possible_states.append((place1, place2, 1))
            possible_states.append((place1, place2, 2))

        possible_states.append((place1, (14, False), 1))
        possible_states.append((place1, (14, False), 2))

    P = {} # probability 1 win
    best_policy = {}
    nb_turn = {}

    nb_turn_solo, _ = value_iteration(layout, circle, 0.001, alpha=1)


    for state in possible_states:
        P[state] = 0
        best_policy[state] = 0
        nb_turn[state] = np.array([0., 0.])
    
    for _ in range(n):
        # print(_)
        delta = 0
        for state in possible_states:
            v = P[state]
            (_, _, whoseturn) = state

            if whoseturn == 2:
                minv = np.inf
                for action in range(3):
                    Pn, new_nb_turn = expected_probability_win(state, action, P, layout, circle, nb_turn, nb_turn_solo)
                    # print(nv)
                    if Pn <= minv:
                        minv = Pn
                        best_policy[state] = action
                        nb_turn[state] = new_nb_turn

                P[state] = minv
            else :  # whoseturn == 1
                maxv = -np.inf
                for action in range(3):
                    Pn, new_nb_turn = expected_probability_win(state, action, P, layout, circle, nb_turn, nb_turn_solo)
                    if Pn >= maxv:
                        maxv = Pn
                        best_policy[state] = action
                        nb_turn[state] = new_nb_turn
                P[state] = maxv
            delta = max(abs(v-P[state]), delta)
        # print(delta)
    return P, best_policy, nb_turn
        