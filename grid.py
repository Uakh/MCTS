#!/usr/bin/env python3
#MCTS

class Grid:

    def __init__(self, width, height):
        """
        Integer -> Integer -> Grid

        Initializes a grid of specified size and all squares set to None
        """
        self.width = width
        self.height = height
        column = []
        for i in range(height):
            column.append(None)
        self.grid = []
        for i in range(width):
            self.grid.append(column.copy())

    def __iter__(self):
        """
        VOID -> Iterable
        """
        return squares()

    def squares(self):
        """
        VOID -> String

        Generates all squares in the grid
        """
        for i in range(self.width):
            for j in range(self.height):
                yield self.grid[i][j]

    def get_chip(self, location):
        """
        String -> String

        Returns the chip value at specified location
        """
        t = self.__l2t(location)
        x = t['x']
        y = t['y']
        return self.grid[x][y]

    def set_chip(self, location, chip):
        """
        String -> VOID

        Sets the chip value at specified location
        Example values:
            None = free
            'B'  = black
            'W'  = white
        """
        t = self.__l2t(location)
        x = t['x']
        y = t['y']
        self.grid[x][y] = chip

    def l2t(self, location):
        """
        String -> {Integer, Integer}

        Translates easy to use string coordinates (eg. DF44) to
        implementation specific wizzzz. Note that A = 0 so B = AB and
        numeration goes A, B, C...Y, Z, BA, BB, BC...
        Digit numbers start from 1, not 0.
        """
        l = location.upper()
        x1 = [ord(a) - 65 for a in l if str.isalpha(a)]
        x = 0
        for i, v in enumerate(x1):
            x += v * pow(26, (len(x1) - i - 1))

        y = int(''.join([a for a in l if str.isnumeric(a)])) - 1
        return {'x': x, 'y': y}

    def t2l(self, token):
        """
        {Integer, Integer} -> String

        Performs the reverse operation of l2t
        All letters before digits since the operation would otherwise
        be ambiguous because l2t isn't injective (ZT9 = Z9T = 9ZT)
        """
        x1 = token['x']
        x = ''
        while x1 > 0:
            a = x1 % 26
            x = chr(a + 65) + x
            x1 = (x1 - a) / 26
        y = str(token['y'] + 1)
        return x+y