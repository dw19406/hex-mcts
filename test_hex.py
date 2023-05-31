"""Module to test agents. Plays out a given number of games with a given training time."""

from hex import Node, Game
import random
import mcts2
import mcts

def random_choice(position):
    """Random choice agent"""
    return(random.choice(position.get_actions()))

def compare_policies(p1, p2, games, size):
    """Function to play out games and determine the number of wins player 1 has."""
    p1_wins = 0
    for i in range(games):
        p1_policy = p1()
        p2_policy = p2()
        position=Game(size)
        while (not position.is_terminal()):
            if position.player==1:
                move = p1_policy(position)
            else:
                move = p2_policy(position)
            position=position.successor(move)
        if position.is_p1_win():
            p1_wins+=1
    return p1_wins

def test_game(count, p1_policy_fxn, p2_policy_fxn):
    wins = compare_policies(p1_policy_fxn, p2_policy_fxn, count, 12)
    print("WINS:", wins, "TOTAL:",count)

if __name__ == '__main__':
    count=50
    time=0.05
    test_game(count, lambda: mcts2.mcts_policy(time),lambda: random_choice) # Not using AMAF
    test_game(count, lambda: mcts.mcts_policy(time),lambda: random_choice) # Using AMAF