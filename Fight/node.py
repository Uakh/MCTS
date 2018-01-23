#!/usr/bin/env python3
#MCTS

import c4
import random
import math
import copy

class Node:

    def __init__(self, father = None, state = None, terminal = False, win = False):
        """
        Node -> Connect4 -> Boolean -> Node

        Initializes a new node of the game tree
        """
        self.N = 0 #Number of visits
        self.Q = 0 #Sum of results
        self.father = father
        if state:
            self.state = state
        else:
            self.state = c4.Connect4()
        self.children = [{"move":x, "node":None} for x in self.state.moves()]
        self.terminal = terminal
        self.win = win

    def play(self, move):
        """
        Integer -> Node

        Returns a move's associated sub-tree
        """
        child = [x for x in self.children if x["move"] == move][0]
        next_root = None
        if (not child["node"]):
            next_root = self.expand(child)
        else:
            next_root = child["node"]
        next_root.father = None
        return next_root

    def UCT_search(self):
        """
        VOID -> VOID

        Performs one iteration of UCT search
        """
        target = self.tree_policy()
        result = -1 * target.default_policy() * target.state.player
        target.backpropagate(result)

    def UCB1(self, node):
        """
        Node -> Numeric

        Returns the UCB1 value of a given node
        """
        C = 2
        exploitation = node.Q / node.N
        exploration = C * math.sqrt(math.log(node.father.N) / node.N)
        return exploitation + exploration

    def best_child(self):
        """
        VOID -> Node

        Returns the node with the highest associated UCB1 value
        """
        K = [{"node":x["node"],
              "value":self.UCB1(x["node"])} for x in self.children]
        return max(K, key=(lambda x: x["value"]))["node"]

    def next_move(self):
        """
        VOID -> Integer

        Returns the most explored 1st move
        """
        K = [(x["node"].N, x["move"]) for x in self.children]
        return max(K, key=(lambda x: x[0]))[1]

    def unexpanded_child(self):
        """
        VOID -> Child

        Returns a random unexpanded child
        Raises IndexError if all children are expanded
        """
        unexpanded = [x for x in self.children if (not x["node"])]
        return random.choice(unexpanded) #Raises IndexError

    def expand(self, child):
        """
        Child -> Node

        Expands a child and returns the associated node
        """
        move = child["move"]
        child_state = copy.deepcopy(self.state)
        child_state.play(move)
        win = self.state.isWin(move)
        terminal = win or (len(child_state.moves()) == 0)
        child_node = Node(self, child_state, terminal, win)
        child["node"] = child_node
        return child_node

    def backpropagate(self, result):
        """
        Numeric -> VOID

        Backpropagates up to the root the result of a simulation
        """
        self.N += 1
        self.Q += result
        if self.father:
           self.father.backpropagate(-1 * result)

    def tree_policy(self):
        """
        VOID -> Node

        Follows UCT algorithm through expanded tree
        """
        if self.terminal:
            return self
        else:
            try:
                child = self.unexpanded_child()
            except IndexError:
                return self.best_child().tree_policy()
            else:
                return self.expand(child)

    def default_policy(self):
        """
        VOID -> Numeric

        Runs an uniformly distributed random simulation from
        the current state until reaching a terminal state
        """
        if self.win:
            return (-1 * self.state.player)
        sim_state = copy.deepcopy(self.state)
        return self._dpol_helper(sim_state)

    def _dpol_helper(self, state):
        """
        Connect4 -> Numeric

        Helper function for default_policy
        """
        try:
            move = random.choice(state.moves())
        except IndexError:
            return 0
        if state.isWin(move):
            return state.player
        else:
            state.play(move)
            return self._dpol_helper(state)