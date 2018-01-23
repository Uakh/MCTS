#!/usr/bin/env python3
#MCTS

import node
import multiprocessing.pool as mp
import time

##Parameters##
#Processes per player
cpu = (1, 4)
#Allowed time per turn in s
think = 3
#Games to play
N = 25
####

def cpu_move(tree):
    t_end = time.monotonic() + think
    while time.monotonic() < t_end:
        tree.UCT_search()
    return tree.next_move()

def vote(pool, roots):
    votes = [pool.apply_async(cpu_move, (t, )) for t in roots]
    votes = [t.get() for t in votes]
    votes = {m:votes.count(m) for m in set(votes)}
    return max(votes.items(), key=(lambda x: x[1]))[0]

def fight():
    S, D, K = 0, 0, 0 #2nd player wins, draws, total turns elapsed
    with mp.Pool(processes=cpu[0]) as pool0, mp.Pool(processes=cpu[1]) as pool1:
        pool = (pool0, pool1)
        for i in range(N):
            root = [[node.Node() for _ in range(p)] for p in cpu]
            flip = i % 2 #Alternate starting player to offset 1st move advantage
            while True:
                K += 1
                next_move = vote(pool[flip], root[flip])
                if root[flip][0].state.isWin(next_move):
                    S += flip
                    break
                for j in range(len(root)):
                    for k in range(len(root[j])):
                        root[j][k] = root[j][k].play(next_move)
                if root[0][0].terminal:
                    D += 1
                    break
                flip = (flip + 1) % 2 #0 <-> 1
    print("N %d\nS %d\nD %d\nK %d" % (N, S, D, K))

if __name__ == "__main__":
    fight()