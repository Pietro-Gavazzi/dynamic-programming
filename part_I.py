"""
LINFO_2275: Data mining and Decision making
Project Part I: Snakes and Ladder

authors: Pietro GAVAZZI, Francis JACOBS, Alex WLODAWER
"""

import numpy as np

def transition(state, action, layout, circle):

    def roll_security_dice():
        trap_triggered = False
        dice_roll = np.random.choice([0, 1])
        return (dice_roll, trap_triggered)

    def roll_normal_dice():
        trap_triggered = np.random.choice([True, False])
        dice_roll = np.random.choice([0, 1, 2])
        return (dice_roll, trap_triggered) 


    def roll_risky_dice():
        trap_triggered = True
        dice_roll = np.random.choice([0, 1, 2, 3])
        return (dice_roll, trap_triggered)
    

    roll_dice_functions = {0:roll_security_dice, 1:roll_normal_dice, 2:roll_risky_dice} 


    (current_position, current_skip_next_turn) = state
    new_skip_next_turn = False

    if current_position == 14:
        print("nice")
        return (current_position, new_skip_next_turn)
    
    if current_skip_next_turn:
        return (current_position, new_skip_next_turn)
    

    # roll dices
    roll_function = roll_dice_functions[action]
    (dice_roll, trap_triggered) =  roll_function()

    # find new position
    if dice_roll==0:
        new_position = current_position
    else: # if dice roll not 0
        if (current_position == 2):
                if np.random.choice([True, False]):
                    new_position = current_position + dice_roll
                else:
                    new_position = 9+dice_roll

        elif  current_position in range(10): # but not 2

            new_position = current_position+dice_roll

            if new_position > 10:
                if circle:
                    new_position -= 10
                else:
                    new_position = 14

        elif current_position in range(10, 14):
            new_position = current_position+dice_roll

            if new_position > 14:
                if circle:
                    new_position -= 14
                else:
                    new_position = 14

    # Deal with the traps
    if trap_triggered:

        trap = layout[new_position]

        if trap == 4:
            trap = np.random.choice([1, 2, 3])

        if   trap == 1:
            new_position = 0

        elif trap == 2:
            if new_position in range(10, 13):
                new_position -= 7 # -7 -3 = -10
            new_position = max(0, new_position - 3)

        elif trap == 3:
            new_skip_next_turn=True

    return (new_position, new_skip_next_turn)

def expected_policy_value(state, action, V, layout, circle, alpha):

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



    Q = 0
    (current_position, current_skip_next_turn) = state

    if current_position == 14:
        new_state = (14, False)
        Q +=  0 + alpha*V[new_state]
        return Q 
    
    if current_skip_next_turn:
        new_state = (current_position, False)
        Q += 1 + alpha*V[new_state]
        return Q
    


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

    list_new_positions_after_traps = []

    for (p, new_position_before_trap, trap_triggered) in list_new_positions_before_traps:
        # Deal with the traps
        trap = layout[new_position_before_trap]

        if  (not trap_triggered) or (trap == 0):
            new_skip_next_turn = False
            new_position_after_trap = new_position_before_trap
            list_new_positions_after_traps.append((p, (new_position_after_trap, new_skip_next_turn)))
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

                list_new_positions_after_traps.append((p, (new_position_after_trap, new_skip_next_turn)))

    # print(list_new_positions_after_traps)
    for (p, new_state) in list_new_positions_after_traps:
        Q +=  p*(1 + alpha*V[new_state])

    return Q

    
def value_iteration(layout, circle, theta, alpha):

    possible_states = []
    for i in range(len(layout)):
        if layout[i]>=3:
            possible_states.append((i, False))
            possible_states.append((i, True))
        else:
            possible_states.append((i, False))

    V = {}
    PI = {}

    for state in possible_states:
        V[state] = 0
        PI[state] = 0
    
    delta = 2*theta
    while delta>=theta:
        delta = 0
        for state in possible_states:
            v = V[state]
            minv = np.inf
            for action in range(3):
                Q = expected_policy_value(state, action, V, layout, circle, alpha)
                # print(nv)
                if Q <= minv:
                    minv = Q
                    PI[state] = action
            V[state] = minv
            delta = max(abs(v-V[state]), delta)
    return V, PI
# %%      

"""
Determines the optimal strategy regarding the choice of dice in the S&L game

Parameters
----------
layout : numpy.ndarray
    Represents the 15 squares of S&L game, each layout[i] represents the type of square:
        0 = ordinary square
        1 = restart trap (go back to square 1)
        2 = penalty trap (go back 3 steps)
        3 = prison trap (skip next turn)
        4 = mystery trap (random trap)
        
circle : bool
    True: player must land exactly on final square to win, otherwise loop back to square 1
    False: player wins as soon as they land on or overstep the final square

Returns
-------
expec : numpy.ndarray
    expected cost for each square (excl. final/goal square)    

dice : numpy.ndarray
    choice of dice for each square (excl. final/goal square)

"""
def markovDecision(layout,circle):
    # Initialize solution arrays
    expec = np.zeros(14) # index 0 = square1; index 13 = square 14
    dice = np.zeros(14) # goal square does not need an optimal action
    
    nTiles = layout.size
    
    V, PI = value_iteration(layout, circle, 0.000000001, alpha=1)
    
    for i in range(nTiles-1):
        expec[i] = V[(i,False)]
        dice[i] = PI[(i,False)]
    
    return [expec, dice]
        

#%%
# Simulate games

circle = False

layouts = []
for i in range(5):
    layout = np.ones(15)*i
    layout[0] = 0
    layout[14] = 0
    layouts += [layout]

for lay in layouts:
    for cir in [False, True]:
        
        E, D = markovDecision(lay, cir)
        print("==========================================================================")
        print("Layout",lay,"Circle =",cir)
        # print(E)
        # print("=============")
        print(D)
        print("Expected number of turns : {:.4f}".format(E[0]))
        # print("==========================================================================")

#%%
# layout = np.random.choice([0, 4], 15, p=[0.5, 0.5])
# layout[0] = 0
# layout[14] = 0
# #%%

# circle = False

# E, D = markovDecision(layout, circle)
# print("==========================================================================")
# print("Layout",layout,"Circle =",circle)
# # print(E)
# # print("=============")
# print(D)
# print("Expected number of turns : {:.4f}".format(E[0]))
# print("==========================================================================")

# #%%
# N  = 10000 #number of games simulated

# die = 2 # strategy with a single dice
# import time

# turns = np.zeros(N)
# tic = time.time()
# for i in range(N):
#     state = (0,False)
#     count = 0
#     while(state[0] != 14):
#         count += 1
#         die = np.random.choice([0, 1, 2]) # assign random die as action
#         state = transition(state, D[state[0]], layout, circle) # modify D[state[0]] with variable die if you want another strategy
#     # print("Game finished in", count, "turns")
#     turns[i] =  count
# tac = time.time()
# print("===========================================================================")
# print("Experimental number of turns :", np.mean(turns),", found in", tac - tic,"s")
# print("Max turns =", np.max(turns), "min turns =", np.min(turns))
