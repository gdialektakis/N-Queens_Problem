import time
from random import randint
from random import random

import numpy as np


class SimulatedAnnealing:

    def __init__(self, suppress, t0, tmin, cool, eps, sn=100):
        self.board = None  # The Queens are represented in this 1d array. The array position and the cell number are the Queen's 'coordinates' in the board.
        self.results = {}  # Dictionary that holds the results of the experiments.
        self.eps = eps  # Epsilon number (ε). Every number below this is considered '0'. This is used to cutoff some very low SA costs that "keep the algo moving".
        self.T0 = t0  # Starting temperature used in SA, can't be set to more that 1.0 or lower than eps (see above).
        self.T_min = tmin  # Ending temperature used in SA, set
        self.cool = cool  # SA cooling factor.
        self.search_neighbours = sn  # Amount of neighbours to search before quitting
        self.suppress = suppress  # Chose whether board and other messages will be printed to stdout.
        self.numOfQueens = None  # Board size
        self.moves = {}  # Average moves done in order to solve the problem

    def __str__(self):
        return '\nSimulated Annealing'

    # Run the algorithm a few times and time it. Board is generated randomly.
    def run(self, start, stop, step, repeat):
        for n in range(start, stop + 1, step):
            run = []
            self.board = list([randint(0, n - 1) for _ in range(n)])  # Start by randomly generating the board.
            moves = 0
            for j in range(repeat):
                start_time = time.time()
                self.numOfQueens = n
                moves = self.anneal(n) / repeat  # Run the algorithm to solve the problem.
                end_time = time.time()
                run.append((end_time - start_time))  # Save the time it took to solve this board and move on.
                self.board[:] = list([randint(0, n - 1) for _ in range(n)])
            self.results[n] = run
            self.moves[n] = moves

    def successor_function(self, n):
        state = self.get_neighbour(self.board, n)
        cost = self.cost(state, n)
        return state, cost

    def anneal(self, n):
        T = self.T0  # Starting temperature
        cool = self.cool  # Cooling factor
        T_min = self.T_min  # Ending temperature
        loops = 0  # This param is used in order to avoid an endless annealing process. It basically stops the loop after 100 times (is usually 1-2).
        moves = -1
        while self.cost(self.board, n) != 0:  # Goal test
            while T - T_min >= self.eps:
                currentCost = self.cost(self.board, n)
                neighbours = self.search_neighbours
                while neighbours > 0:
                    nextState, nextCost = self.successor_function(n)  # Get the next state
                    moves += 1  # Count the new move (used for statistics later on)
                    e = (np.float128) = -(nextCost - currentCost) / T  # This kills our performance but stops an arithmetic overflow.
                    if np.exp(e) > random():  # Perform the SA standard check
                        self.board = nextState  # Jump to the next state.
                        currentCost = nextCost
                        if currentCost == 0:  # Goal test
                            self.print_board()
                            return moves
                    neighbours -= 1
                T *= cool

            # If the original hyper params weren't good enough, adapt and retry.
            cool = min(1 - self.eps, cool * 1.1)  # Increase the cooling factor (so it cools slower !!) by 10% but don't go over 1.0.
            T = self.T0
            T_min = self.T_min
            loops += 1
            if not self.suppress:
                print('Adapting: {0} {1} {2} No{3}'.format(T, cool, T_min, loops), flush=True)
            if loops > 100:
                print("\n\nToo many loops...")  # Mostly for debug or REALLY bad hyper params.
                exit(-2)

    @staticmethod
    def get_neighbour(queens, n):  # Chose a random neighbour to jump to.
        queensTemp = queens[:]
        queensTemp[randint(0, n - 1)] = randint(0, n - 1)
        return queensTemp[:]

    @staticmethod
    def cost(queens, n):  # Counts the number of conflicts across the board.
        conflicts = 0
        for i in range(n):
            for j in range(i + 1, n):
                if i != j and (queens[i] == queens[j] or abs(queens[i] - queens[j]) == abs(i - j)):  # Horizontally and diagonally
                    conflicts += 1
        return conflicts

    def print_board(self):
        if self.suppress:  # Don't print if suppress is enabled.
            return
        print('\n\n\n{2} solution for {0} queens flat board: {1}'.format(self.numOfQueens, self.board, self))
        to_print = ''
        for r in range(len(self.board)):
            for c in range(len(self.board)):
                if self.board[c] == r:
                    to_print += "Q "
                else:
                    to_print += "x "
            to_print += "\n"
        print(to_print)
