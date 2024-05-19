"""
LINFO_2275: Data mining and Decision making
Project Part II: Two players

authors: Pietro GAVAZZI, Francis JACOBS, Alex WLODAWER
"""


import numpy as np
from part_I import  value_iteration



# %%     

#  Calculates from an initial place the expected new places and there probabilities after rolling the dice and encountering traps.
def expected_new_places(state, action, layout, circle):

    # Nested functions for different dice rolls and their probabilities
    def rolls_security_dice():
        possible_trap_triggered = [False]
        possible_dice_rolls = [0, 1]
        p = 1/2
        return [(p, trap_triggered, dice_roll) for trap_triggered in possible_trap_triggered for dice_roll in possible_dice_rolls]    

    def rolls_normal_dice():
        possible_trap_triggered = [True, False]
        possible_dice_rolls = [0, 1, 2]
        p = 1/6
        return [(p, trap_triggered, dice_roll) for trap_triggered in possible_trap_triggered for dice_roll in possible_dice_rolls]    

    def rolls_risky_dice():
        possible_trap_triggered = [True]
        possible_dice_rolls = [0, 1, 2, 3]
        p = 1/4
        return [(p, trap_triggered, dice_roll) for trap_triggered in possible_trap_triggered for dice_roll in possible_dice_rolls]    

    rolls_dice_functions = {0:rolls_security_dice, 1:rolls_normal_dice, 2:rolls_risky_dice} 


    (current_position, current_skip_next_turn) = state

    if current_skip_next_turn:
        new_place = (current_position, False)
        return [(1, new_place)]
    

    # roll dices
    roll_function = rolls_dice_functions[action]
    list_rolls =  roll_function()

    list_new_positions_before_traps = []

    for (p, trap_triggered, dice_roll) in list_rolls:
        # find new position
        if dice_roll==0:
            new_position_before_trap = current_position
            list_new_positions_before_traps.append((p, new_position_before_trap, trap_triggered))
        else: # dice roll is not 0
            if (current_position == 2):
                    new_position_before_trap = current_position + dice_roll
                    list_new_positions_before_traps.append((p*1/2, new_position_before_trap, trap_triggered))
                    new_position_before_trap = 9+dice_roll
                    list_new_positions_before_traps.append((p*1/2, new_position_before_trap, trap_triggered))


            elif  current_position in range(10): # but not 2
                new_position_before_trap = current_position+dice_roll
                if new_position_before_trap > 10:
                    if circle:
                        new_position_before_trap -= 10
                    else:
                        new_position_before_trap = 14
                list_new_positions_before_traps.append((p, new_position_before_trap, trap_triggered))

            elif current_position in range(10, 14):
                new_position_before_trap = current_position+dice_roll
                if new_position_before_trap > 14:
                    if circle:
                        new_position_before_trap -=14
                    else:
                        new_position_before_trap = 14
                list_new_positions_before_traps.append((p, new_position_before_trap, trap_triggered))

    list_new_places_after_traps = []

    for (p, new_position_before_trap, trap_triggered) in list_new_positions_before_traps:
        # Deal with the traps
        trap = layout[new_position_before_trap]

        if  (not trap_triggered) or (trap == 0):
            new_skip_next_turn = False
            new_position_after_trap = new_position_before_trap
            list_new_places_after_traps.append((p, (new_position_after_trap, new_skip_next_turn)))
        else:
            trap_list = []

            if trap == 4:
                trap_list.append(1)
                trap_list.append(2)
                trap_list.append(3)
                p/=3
            else:
                trap_list.append(trap)
            
            for trap in trap_list:
                if   trap == 1:
                    new_position_after_trap = 0
                    new_skip_next_turn = False

                elif trap == 2:
                    new_position_after_trap = new_position_before_trap
                    if new_position_after_trap in range(10, 13):
                        new_position_after_trap -= 7 # -7 -3 = -10
                    new_position_after_trap = max(0, new_position_after_trap - 3)
                    new_skip_next_turn = False


                elif trap == 3:
                    new_position_after_trap = new_position_before_trap
                    new_skip_next_turn=True

                list_new_places_after_traps.append((p, (new_position_after_trap, new_skip_next_turn)))

    return list_new_places_after_traps



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
def min_max(layout, circle, theta):
    
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
    
    delta = 2*theta
    while delta>=theta:
        print(delta)
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
    print(delta)
    return P, best_policy, nb_turn
        

# %%     

# circle: a boolean variable (type bool), indicating if the player must land exactly on
# the final, goal, square 15 to win (circle = True) or still wins by overstepping the final
# square (circle = False).
circle = True

# layout: a vector of type numpy.ndarray that represents the layout of the game, containing 15 values
#         representing the 15 squares of the Snakes and Ladders game:
# layout[i] = 0 if it is an ordinary square
#           = 1 if it is a “restart” trap (go back to square 1)
#           = 2 if it is a “penalty” trap (go back 3 steps)
#           = 3 if it is a “prison” trap (skip next turn)
#           = 4 if it is a “mystery” trap (random effect among the three previous)
# Note that the first and final squares cannot be trapped.

np.random.seed(42)
layout = np.random.choice([1, 2, 3, 4], 15)
layout[0] = 0
layout[14] = 0

P, best_policy, nb_turn = min_max(layout, circle, 0.000000001)

print(nb_turn)
# %%
