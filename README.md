To run the program, run test_hex.py

This program implements Monte Carlo Tree Search (MCTS) for the game of Hex, a two-player game played on a board of hexagonal tiles, as shown below.

![An 11x11 Hex board](hex%20board.png)

Each player has two opposite sides on this board, and they take turns placing their piece on an unoccupied hex. The winner is the one who connects their two sides first. This game is perfect for MCTS, as:
* The game is finite
* There are no draws
* The state space is too complex for a brute force solution in reasonable time

However, traditional MCTS suffers in more complex games, as the computation time is very high. As a result, optimizations such as All-Moves-As-First (AMAF) can be used to allow for a faster convergence upon an ideal solution.

This program creates two MCTS agents. One has AMAF optimizations, and the other does not. Testing the programs after allowing a certain amount of time for tree search allows for the effectiveness of the optimizations to be seen. Both MCTS policies are selected to play first against a random agent. This is because, in the game of Hex, the first player always has a winning strategy (This can be argued via symmetry: should the first player occupy the center-most square initially, every subsequent move can be a mirror of the opponent's move. Since the first player must be at least as good as the second player, they can never lose and thus must win). Since both MCTS agents should converge to ideal play given enough time, this methodology is most effective to demonstrate the difference in convergence time.

The difference in convergence time is evident: MCTS with AMAF significantly outperforms standard MCTS so long as MCTS is not given enough time to fully converge. This can result in incredibly high differences in win ratios.