# Introduction
This code comes from a university group's assignment we received for a lesson in dynamic programming (Markov Decision Processes and Reinforcement Learning, LSINF2275 - Data Mining and Decision Making, UCLouvain).

The instructions were lost, but based on our own report I tried to reconstruct roughly what was asked.

# Part 1
This part was the same for every group. From what I can tell, the assignment was to model a **single-player game of Snakes and Ladders on a 15-tile board** as a Markov Decision Process, and to find the optimal strategy (i.e., which dice to choose on each tile) using the **value iteration** algorithm.

The rules I reconstructed:
- The board can be either **circular** or **non-circular**. On a non-circular board, overshooting tile 15 sends you back to the start; on a circular one you simply wrap around, or in some layout variants you must land on tile 15 exactly to win.
- Certain tiles can be **trapped**, with different trap types (e.g., sending the player back to the start, moving them back 3 steps, or making them skip their next turn).
- On each non-blocked turn, the player must choose **which of several dice to roll**. Each dice has a different distribution of outcomes, and therefore a different risk of triggering a trap versus a different expected speed of progress.
- The objective is to **win as fast as possible**, i.e., to minimize the expected number of turns needed to reach tile 15.

We modeled this as an MDP where:
- a state is a tuple `(position, blocked)`,
- the immediate cost of any action is 1 (one turn spent),
- `V(k)` is the minimum expected number of turns to reach the goal from state `k`,
- the optimal policy is found by iterating the Bellman equation until convergence.

We tested this on several layouts (no traps, only-trap variants, a random mixed layout) and compared the theoretical expected number of turns against simulated results over 10,000 games, confirming the two matched closely. We also compared the optimal policy against naive baselines (always dice 0 / dice 1 / dice 2 / random dice) to show it outperforms them.

# Part 2
In this second part, the teacher let us extend the project in any way we decided. From what we wrote in the report, I suppose part of the assignment was to make this extension "interesting in a business world."

We decided to extend the game into a **competitive, two-player version**, where both players race to reach tile 15 first, and we computed the optimal strategy for each player using a **min-max algorithm** applied to the same MDP framework (now tracking both players' positions and whose turn it is, and optimizing the probability of winning rather than the expected number of turns).

We made the interesting discovery that the strategy which maximizes expected value (i.e., the fastest expected finish, from Part 1) is *not* the same as the strategy that maximizes the probability of winning in a competitive setting:
- When our player is lagging behind, it will take more risks to try to make up for its disadvantage.
- Similarly, when our player is in front, it will take the less risky dice to make sure it doesn't fall into a trap.

