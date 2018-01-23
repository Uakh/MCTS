#!/usr/bin/env python3
#MCTS

import cmd
import node
import os
import multiprocessing

def cpu_move(root, cpu_count):
    for _ in range(15000):
        root.UCT_search()
    return root.next_move()

class C4Shell(cmd.Cmd):
    intro = "\nConnect 4 MCTS solver. Type help or ? to list commands.\n"
    prompt = "(human X) "
    root = None
    cpu_count = 0

    def do_play(self, arg):
        """
        Play a move in given column: play [0-6]
        """
        exit = self.play(arg)
        self.graph()
        return exit

    def play(self, arg):
        """
        Play a move in given column: play [0-6]
        """
        #Human
        try:
            move = int(arg.split()[0])
        except (ValueError, IndexError):
            print("Invalid move")
            return False
        if self.root[0].state.isWin(move):
            print("human wins")
            return True
        try:
            for i in range(len(self.root)):
                self.root[i] = self.root[i].play(move)
        except IndexError:
            print("Invalid move")
            return False
        if self.root[0].terminal:
            print("Draw")
            return True
        #CPU
        # for _ in range(15000):
        #     self.root.UCT_search()
        # next_move = self.root.next_move()
        with multiprocessing.Pool() as pool:
            votes = [pool.apply_async(cpu_move, (t, self.cpu_count)) for t in self.root]
            votes = [t.get() for t in votes]
        votes = {m:votes.count(m) for m in set(votes)}
        next_move = max(votes.items(), key=(lambda x: x[1]))[0]
        print("(CPU O) %d" % next_move)
        if self.root[0].state.isWin(next_move):
            print("CPU wins")
            return True
        for i in range(len(self.root)):
            self.root[i] = self.root[i].play(next_move)
        if self.root[0].terminal:
            print("Draw")
            return True

    def do_print(self, arg):
        """
        Print the current game grid: print
        """
        self.graph()
        return False

    def graph(self):
        """
        Prints the current game grid
        """
        print()
        print('\n'.join(['│'.join(['{:1}'.format(self.parse(token)) for token in column]) for column in list(zip(*self.root[0].state.grid))[::-1]]))
        print('─┴─┴─┴─┴─┴─┴─')
        print(' '.join([str(i) for i in range(7)]))
        print()

    def parse(self, token):
        if (token == 1):
            return 'O'
        elif (token == -1):
            return 'X'
        else:
            return ''

    def do_q(self, arg):
        """
        Quit the program: q
        """
        return True

    def preloop(self):
        self.cpu_count = (os.cpu_count() // 2) or 1
        self.root = [node.Node() for _ in range(self.cpu_count)]

if __name__ == '__main__':
    C4Shell().cmdloop()