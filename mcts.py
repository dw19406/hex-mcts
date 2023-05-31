"""Monte Carlo Tree Search implementation with AMAF optimization."""

import math
import random
import time

def choose_next_node(state_dict,path,actions_set):
    """Function to choose next node.
    Will use UCB to find an unexplored node, then randomply explore from
    that node until reaching a terminal node.
    """
    state=path[-1]
    actions=state.get_actions()
    if len(actions)==0 or actions[0] is None:
        backtrack(state_dict,path,state.payoff(), actions_set)
        return 0
    successors=[]
    for i in actions:
        successors.append(state.successor(i))
    for ind, succ in enumerate(successors):
        if not (succ in state_dict):
            #Proceed down state.successor(i) until end
            path.append(succ)
            actions_set.append(actions[ind])            
            score=(traverse_tree_to_end(path, actions_set))
            backtrack(state_dict,path,score, actions_set)
            return 0
    scores=[0]*len(actions)
    act=state.actor()
    for ind, succ in enumerate(successors):
        succ_dict_ref=state_dict[succ]
        scores[ind]=succ_dict_ref[0]/succ_dict_ref[1]+(act-0.5)*(-2)*math.sqrt(2*math.log(state_dict[state][1])/succ_dict_ref[1])
    best_score_index=0
    if act==0:
        best_score_index=scores.index(max(scores))
    else:
        best_score_index=scores.index(min(scores))
    path.append(successors[best_score_index])
    actions_set.append(actions[best_score_index])
    return 1

def traverse_tree_to_end(path, actions_set):
    """Function to search down a tree until reaching a terminal node
    Returns the payoff of the terminal node
    """
    curr_state=path[-1]
    while not curr_state.is_terminal():
        act=random.choice(curr_state.get_actions())
        curr_state=curr_state.successor(act)
        actions_set.append(act)
    return curr_state.payoff()

def backtrack(state_dict, path, payoff, actions_set):
    """Function to trace back up the path and update everything from
    the point of origin (root) to the last discovered node.
    """
    for point in path:
        if point in state_dict:
            state_dict[point][0]+=payoff
            state_dict[point][1]+=1
        else:
            state_dict[point]=[payoff,1]
    for ind, act in enumerate(actions_set[2:]):
        if ind%2==0:
            succ=path[0].successor(act)
            if succ in state_dict:
                state_dict[succ][0]+=payoff
                state_dict[succ][1]+=1
            else:
                state_dict[succ]=[payoff,1]


def search(state_dict, path, actions_set):
    """Function to facilitate searching"""
    curr_state=1
    while not (curr_state==0):
        curr_state=choose_next_node(state_dict,path,actions_set)
    return

def mcts_policy(cpu_time):
    """Function to generate a Monte Carlo Tree Search policy"""
    def ret_function(state):
        """The Monte Carlo Tree Search policy"""
        state_dict={}
        start = time.time()
        if state.is_terminal() or state.get_actions()[0] is None:
            return None
        actions_set=[]
        while time.time() - start < cpu_time: #Run for a given amount of time
            actions_set=[]
            search(state_dict, [state], actions_set)
        max_iters=-10000
        best_action=None
        actions=state.get_actions()
        for i in actions:
            next_state=state.successor(i)
            if next_state in state_dict:
                if state_dict[next_state][0]>max_iters:
                    best_action=i
                    max_iters=state_dict[next_state][0]
        return best_action
    return ret_function