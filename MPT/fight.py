#!/usr/bin/env python3
#MCTS

import node
import multiprocessing.pool as mp

##Parameters##
#Processes per player
cpu1 = 1
cpu2 = 4
#Allowed time per turn in s
think = 1
#Games to play
N = 100
####
W, D, L = 0, 0, 0
with mp.Pool(processes=cpu1) as pool1, mp.Pool(processes=cpu2) as pool2:
    for game in range(N):
        roots1 = [node.Node() for _ in range(cpu1)]
        roots2 = [node.Node() for _ in range(cpu2)]
        while True:
