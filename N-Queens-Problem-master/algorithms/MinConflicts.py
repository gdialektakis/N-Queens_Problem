import random
import time


class MinConflicts(object):
    def __init__(self, suppress):
        self.numOfQueens = None
        self.board = []
        self.candidates = []
        # for experiments
        self.results = {}
        self.moves = {}
        self.suppress = suppress

    def __str__(self):
        return '\nMin Conflicts'

    def run(self, start, stop, step, repeat):
        for n in range(start, stop + 1, step):
            run = []
            moves = 0
            for j in range(repeat):
                start_time = time.time()
                self.initialize_board(n)
                moves += self.solve() / repeat
                end_time = time.time()
                run.append((end_time - start_time))
            self.results[n] = run
            self.moves[n] = moves

    def initialize_board(self, numOfRows):  # min_conflict is used to determine the bast placement
        self.candidates = []
        self.board = []
        self.numOfQueens = numOfRows
        for col in range(self.numOfQueens):  # iterates through the columns to place the queen
            self.candidates = []  # Flush the candidates array
            min_conflict = self.numOfQueens
            self.board.append(0)  # finds the rows with the least number of conflicts and adds them to the candidates array
            for row in range(len(self.board)):
                num_of_conflicts = self.check_conflicts(self.board[row], col)
                if num_of_conflicts == min_conflict:
                    self.candidates.append(row)
                elif num_of_conflicts < min_conflict:
                    self.candidates = []
                    self.candidates.append(row)
                    min_conflict = num_of_conflicts
            # selects a random row from the suitable candidates array
            if self.candidates:
                self.board[col] = random.choice(self.candidates)

    # Function to solve the board. uses a while loop to repeat itself. returns the number of turns it took to solve
    def solve(self):
        number_of_moves = 0
        while True:
            num_of_conflicts = 0
            self.candidates = []
            for val in range(len(self.board)):  # Checks for the boards total conflicts
                num_of_conflicts += self.check_conflicts(self.board[val], val)
            if num_of_conflicts == 0:  # If there are no conflicts on the board return the moves
                self.print_board()
                return number_of_moves
            random_queen = random.randint(0, len(self.board) - 1)  # Choose a random queen to move and increase the move counter
            self.successor_function(random_queen)  # Populates the self.candidates array
            if self.candidates:  # If there are candidates set the queen.
                self.board[random_queen] = random.choice(self.candidates)
            number_of_moves += 1  # One more move has been made.

    def successor_function(self, queen):
        self.candidates = []  # Init the candidate array
        min_conflict = self.numOfQueens  # Assume this many conflicts
        for val in range(len(self.board)):  # Finds the rows with the least number of conflicts and adds them to the candidates array
            conflict_num = self.check_conflicts(val, queen)
            if conflict_num == min_conflict:  # Add new candidate
                self.candidates.append(val)
            elif conflict_num < min_conflict:  # Found an objectively better choice, flush the candidate array and add just this choice.
                self.candidates = []
                min_conflict = conflict_num
                self.candidates.append(val)

    # Returns the number of conflicts (cost function)
    def check_conflicts(self, row, col):
        conflict_counter = 0
        # Iterates through the rows and check for possible placements
        for val in range(len(self.board)):
            if val != col:  # Do not count against yourself
                next_queen_row = self.board[val]
                if next_queen_row == row or abs(next_queen_row - row) == abs(val - col):
                    conflict_counter += 1
        return conflict_counter

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
