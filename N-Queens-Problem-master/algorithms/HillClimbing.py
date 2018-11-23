import time
from random import randint


class HillClimbing:
    """Explore the given space by selecting the neighbour with the minimal cost.
     If no improvement can be made restart with a new random set of queen positions.
     This algorithm is used as a baseline for the following experiments.It's supposed to be bad :)"""

    def __init__(self, iterations, suppress, min_cost):
        self.board = None
        self.iterations = iterations
        self.suppress = suppress
        self.min_cost = min_cost
        self.results = {}
        self.moves = {}
        self.numOfQueens = None

    def __str__(self):
        return '\nHill Climbing'

    def run(self, start, stop, step, repeat):
        for n in range(start, stop + 1, step):
            run = []
            self.board = list([randint(0, stop - 1) for _ in range(stop)])
            moves = 0
            for _ in range(repeat):
                start_time = time.time()
                self.numOfQueens = n
                moves = self.climb(stop) / repeat
                end_time = time.time()
                run.append((end_time - start_time))
                self.board[:] = list([randint(0, stop - 1) for _ in range(stop)])
            self.results[n] = run
            self.moves[n] = moves

    def climb(self, stop):
        moves = 0
        while self.cost(self.board, stop) != 0:  # Primary Goal test
            self.board = list([randint(0, stop - 1) for _ in range(stop)])  # Generate random board.
            for x in range(self.iterations):
                if self.cost(self.board, stop) != 0:  # Primary Goal test
                    moves += self.successor_function(self.board, stop)
        self.print_board()
        return moves

    def successor_function(self, queens, n):
        moves = 0
        queensTemp = queens[:]
        minCost = self.min_cost
        bestColumn = None
        bestRow = None
        for i in range(n):  # iterate through queens
            for j in range(n):  # iterate through rows
                if j == queens[i]:  # check if the queen is in the same position
                    j += 1
                    continue
                queensTemp[i] = j  # move queen to the next row
                moves += 1  # Count the move
                cost = self.cost(queensTemp, n)  # determine cost for current position
                if cost < minCost:
                    bestColumn = i  # store the best position and its cost so far
                    bestRow = j
                    minCost = cost
            queensTemp = queens[:]
        self.board[bestColumn] = bestRow
        return moves

    @staticmethod
    def cost(queens, n):  # Counts the number of conflicts across the board.
        conflicts = 0
        for i in range(n):
            for j in range(i + 1, n):
                if i != j and (queens[i] == queens[j] or abs(queens[i] - queens[j]) == abs(i - j)):  # Horizontally and diagonally
                    conflicts += 1
        return conflicts

    def print_board(self):
        if self.suppress:
            return
        print('\n\n\n{2} solution for {0} queens flat board: {1}.'.format(self.numOfQueens, self.board, self))
        to_print = ''
        for r in range(len(self.board)):
            for c in range(len(self.board)):
                if self.board[c] == r:
                    to_print += "Q "
                else:
                    to_print += "x "
            to_print += "\n"
        print(to_print)
