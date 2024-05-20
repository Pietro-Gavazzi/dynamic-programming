# -*- coding: utf-8 -*-
"""
Tests for part_II
"""
from part_II import min_max, value_iteration
import numpy as np
# %%     

# circle: a boolean variable (type bool), indicating if the player must land exactly on
# the final, goal, square 15 to win (circle = True) or still wins by overstepping the final
# square (circle = False).
circle = False

# layout: a vector of type numpy.ndarray that represents the layout of the game, containing 15 values
#         representing the 15 squares of the Snakes and Ladders game:
# layout[i] = 0 if it is an ordinary square
#           = 1 if it is a “restart” trap (go back to square 1)
#           = 2 if it is a “penalty” trap (go back 3 steps)
#           = 3 if it is a “prison” trap (skip next turn)
#           = 4 if it is a “mystery” trap (random effect among the three previous)
# Note that the first and final squares cannot be trapped.

np.random.seed(16)
layout = np.random.choice([0, 4], 15, p=[0.5, 0.5])

print(layout)

layout[0] = 0
layout[14] = 0

P, best_policy, nb_turn = min_max(layout, circle, 100)

E, dice = value_iteration(layout, circle, 0.0001, alpha=1)
    
for key, value in best_policy.items():
    if(key[2] == 2 and key[1][0] != 14 and not key[0][1] and not key[1][1] and value != dice[(key[0])]):
        # print(key, value)
        print(key[0][0]+1, "& ",key[1][0]+1,"& ",value, "&", dice[(key[0])], " \\\\")

# print(dice)

#%%
# print(E)
# for key, value in nb_turn.items():
#     if(key[0][0] == 0):
#         print(key, value)
#     # print(key[0][0]+1, "& ",key[1][0]+1,"& ",value, "&", dice[(key[0])], " \\\\")