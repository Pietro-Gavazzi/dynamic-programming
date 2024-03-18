"""
LINFO_2275: Data mining and Decision making
Project Part I: Snakes and Ladder

authors: Pietro GAVAZZI, Francis JACOBS, Alex WLODAWER
"""

import numpy as np


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
    
    # Implement Value-iteration algo and return optimal policy
    
    
    return [expec, dice]