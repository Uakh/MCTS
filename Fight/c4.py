#!/usr/bin/env python3
#MCTS

import grid

class Connect4(grid.Grid):

    def __init__(self):
        """
        VOID -> Connect4

        Initializes an empty 7x6 Connect4 state
        """
        super().__init__(7, 6)
        self.player = -1
        self.top = [0 for _ in range(7)]

    def isLegal(self, column):
        """
        Integer -> Boolean

        Returns whether a move is legal
        ie. whether the column is not full
        """
        return (not self.grid[column][self.height - 1])

    def isWin(self, column):
        """
        Integer -> Boolean

        Returns whether a move results in a win
        """
        row = self.top[column]
        orig = (column, row)
        vect = ((0, -1), (1, -1), (1, 0), (1, 1))
        for v in vect:
            n = self._aligned(orig, v)
            if (n > 3):
                return True
        return False

    def _aligned(self, origin, vector):
        """
        (Integer, Integer) -> (Integer, Integer) -> Integer

        Returns how many chips of the same color are
        aligned along the direction of a vector

        Note: this is the iterative implementation, a wholemeal
        approach (slice and max) might be more efficient, should
        benchmark that if this method lights up in the profiler.
        """
        x, y = origin[0], origin[1]
        vx, vy = vector[0], vector[1]
        chip = None
        aligned = 1
        for z in (-1, 1):
            for i in range(1, 7):
                dx = x + vx * z * i
                dy = y + vy * z * i
                if ((dx < 0) or (dy < 0)):
                    break
                try:
                    chip = self.grid[dx][dy]
                except IndexError:
                    break
                if (chip == self.player):
                    aligned += 1
                else:
                    break
        return aligned

    def moves(self):
        """
        VOID -> [Integer]

        Returns a generator of legal moves
        """
        return [x for x in range(self.width) if self.isLegal(x)]

    def play(self, column):
        """
        Integer -> VOID

        Returns a new game state instance after a
        given move by the current player
        """
        #Much less painful to slice chars, see _aligned() docstring
        #chr(60) = '<', chr(62) = '>'
        #token = chr(61 + self.player)
        self.grid[column][self.top[column]] = self.player
        self.top[column] += 1
        self.player *= -1

    def _top(self, column):
        """
        Integer -> Integer

        Returns column top index
        ie. lowest empty square
        """
        for i in range(self.height):
            if (not self.grid[column][i]):
                return i