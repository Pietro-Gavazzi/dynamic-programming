"""
File for the tests on part_I
"""
from part_I import markovDecision, transition
import numpy as np
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

# %%
layout = np.random.choice([0, 4], 15, p=[0.5, 0.5])
layout[0] = 0
layout[14] = 0
#%%

circle = False

E, D = markovDecision(layout, circle)
print("==========================================================================")
print("Layout",layout,"Circle =",circle)
# print(E)
# print("=============")
print(D)
print("Expected number of turns : {:.4f}".format(E[0]))
print("==========================================================================")

#%%
N  = 10000 #number of games simulated

die = 2 # strategy with a single dice
import time

turns = np.zeros(N)
tic = time.time()
for i in range(N):
    state = (0,False)
    count = 0
    while(state[0] != 14):
        count += 1
        die = np.random.choice([0, 1, 2]) # assign random die as action
        state = transition(state, D[state[0]], layout, circle) # modify D[state[0]] with variable die if you want another strategy
    # print("Game finished in", count, "turns")
    turns[i] =  count
tac = time.time()
print("===========================================================================")
print("Experimental number of turns :", np.mean(turns),", found in", tac - tic,"s")
print("Max turns =", np.max(turns), "min turns =", np.min(turns))
