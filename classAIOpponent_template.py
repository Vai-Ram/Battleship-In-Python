import random
from classPlayer_template import Player
from classBoard_template import WATER, HIT, MISS, SHIP
import classBoard_template
from classShip_template import Ship

class AIOpponent(Player):
    def __init__(self, name="Bot 9000"):
        # Initialize the AI Opponent.
        super().__init__(name)
        self.hunting = True
        self.target_stack = []
        self.parity = 2
        self.score_grid = [[0 for i in range(10)] for i in range(10)]
        self.needs_recalc = True

    def _get_smallest_alive_ship(self, enemy_board):
        """
        Helper method to find the smallest ship that is NOT sunk.
        """
        smallest_ship_size = 6

        for ship in enemy_board.ships:
            if not ship.is_sunk():
                if smallest_ship_size > ship.size:
                    smallest_ship_size = ship.size

        if smallest_ship_size > 5:
            return 1
        
        return smallest_ship_size

    def update_parity(self, enemy_board):
        """
        Checks if the parity jump distance needs to change.
        """
        curr_parity = self._get_smallest_alive_ship(enemy_board)

        if curr_parity != self.parity:
            self.parity = curr_parity
            self.needs_recalc = True

    def calc_scores(self, enemy_board):
        """
        Performs the full Dynamic Parity and Bridge Check scoring.
        """
        def check(r, c):
            if 0 <= r < 10 and 0 <= c < 10 and enemy_board.grid[r][c] not in (HIT, MISS):
                return 1
            return 0
            
        self.score_grid = [[0 for i in range(10)] for i in range(10)]
        for row in range(10):
            for col in range(10):
                if (row + col) % self.parity == 0:
                    self.score_grid[row][col] += (
                        all(check(row + i, col) for i in range(1, self.parity)) +
                        all(check(row, col + i) for i in range(1, self.parity)) +
                        all(check(row - i, col) for i in range(1, self.parity)) +
                        all(check(row, col - i) for i in range(1, self.parity))
                        )
        
        # FOR TESTING DO NOT REMOVE PLSSS
        for i in self.score_grid: 
            print(*i)
        self.needs_recalc = False
                    
    def patch_scores(self, row, col):
        # HarishWasHere
        """
        The Smart Cache: Locally downgrades scores around a Miss.
        """
        self.score_grid[row][col] = 0
        dist = self.parity        

        if (0 <= col + dist < 10 and self.score_grid[row][col + dist] > 0): 
            self.score_grid[row][col + dist] -= 1

        if (0 <= row + dist < 10 and self.score_grid[row + dist][col] > 0): 
            self.score_grid[row + dist][col] -= 1

        if (0 <= col - dist < 10 and self.score_grid[row][col - dist] > 0): 
            self.score_grid[row][col - dist] -= 1

        if (0 <= row - dist < 10 and self.score_grid[row - dist][col] > 0): 
            self.score_grid[row - dist][col] -= 1

    def hunt(self):
        """
        Finds the highest scored parity square(s) and picks one.
        """
        # HarishWasHereToo
        max_score = max([max(row_score) for row_score in self.score_grid])
        max_score_tuples = []

        for row in range(10):
            for col in range(10):
                # FIX: Check if the tuple (row, col) is in shots_fired
                if self.score_grid[row][col] == max_score and (row, col) not in self.shots_fired:
                    max_score_tuples.append((row, col))

        if max_score_tuples:
            chosen_one = random.choice(max_score_tuples)
        else:
            row, col = random.randint(0, 9), random.randint(0, 9)
            while (row, col) in self.shots_fired:
                row, col = random.randint(0, 9), random.randint(0, 9)
            
            chosen_one = (row, col)

        return chosen_one

    def target(self):
        """
        Pops a coordinate from the stack to finish off a hit ship.
        """
        while self.target_stack:
            element_index = self.target_stack.pop()
            if element_index not in self.shots_fired:
                return element_index

        self.hunting = True
        return self.hunt()

    def attack(self, enemy_board):
        """
        Overrides the Human attack to use the AI Brain.
        """
        def check(r, c):
            if 0 <= r < 10 and 0 <= c < 10 and enemy_board.grid[r][c] not in (HIT, MISS):
                return 1
            return 0

        self.update_parity(enemy_board)

        if self.needs_recalc:
            self.calc_scores(enemy_board)

        if self.hunting:
            row, col = self.hunt()
        else:
            row, col = self.target()

        # FIX: Capture the return value of receive_attack!
        result = enemy_board.receive_attack(row, col)
        self.shots_fired.add((row, col))
        print(f"AI fired at {row}, {col} and the result was {result}")

        # FIX: Match on the captured result, not the grid value
        match result:
            case "MISS":
                if self.hunting:
                    self.patch_scores(row, col)
            case "HIT":
                self.hunting = False
                targets = [(row+1, col), (row-1, col), (row, col+1), (row, col-1)]
                for i, j in targets:
                    if check(i, j):
                        self.target_stack.append((i, j))
            case "SUNK":
                self.hunting = True
                self.target_stack = []
                self.needs_recalc = True

        return result
