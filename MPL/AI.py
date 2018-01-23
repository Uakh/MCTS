#!/usr/bin/env python3
#MCTS

import cmd
import node
import os

class C4Shell(cmd.Cmd):
    intro = "\nConnect 4 MCTS solver. Type help or ? to list commands.\n"
    prompt = "(human X) "
    root = None

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
        if self.root.state.isWin(move):
            print("human wins")
            return True
        try:
            self.root = self.root.play(move)
        except IndexError:
            print("Invalid move")
            return False
        if self.root.terminal:
            print("Draw")
            return True
        #CPU
        iterations = int(15000 / (os.cpu_count() or 1))
        for _ in range(iterations):
            self.root.UCT_search()
        next_move = self.root.next_move()
        print("(CPU O) %d" % next_move)
        if self.root.state.isWin(next_move):
            print("CPU wins")
            return True
        self.root = self.root.play(next_move)
        if self.root.terminal:
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
        print('\n'.join(['│'.join(['{:1}'.format(self.parse(token)) for token in column]) for column in list(zip(*self.root.state.grid))[::-1]]))
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
        self.root = node.Node()

if __name__ == '__main__':
    C4Shell().cmdloop()