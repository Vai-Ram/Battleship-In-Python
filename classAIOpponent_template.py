import random
from unittest import result
from classPlayer_template import Player
from classBoard_template import WATER, HIT, MISS, SHIP
import classBoard_template

class AIOpponent(Player):
    def __init__(self, name="Bot 9000"):
        # Initialize the AI Opponent.
        super().__init__(name)
        self.hunting = True
        self.target_stack = []
        self.parity = 2
        self.score_grid = [[0 for i in range(10)] for i in range(10)]
        self.needs_recalc = True
        self.start=None
    def _get_smallest_alive_ship(self, enemy_board):
        
        """
        Helper method to find the smallest ship that is NOT sunk.
        
        Iterate through enemy_board.ships.
        Filter out the ships where is_sunk() is True.
        Return the minimum 'size' of the remaining ships.
        Handle the edge case: If all ships are somehow sunk, just return 1 to avoid errors.
        """

        smallest_ship_size = 6

        for ship in enemy_board.ships:
            if not ship.is_sunk():
                if smallest_ship_size>ship.size:
                    smallest_ship_size=ship.size

        if smallest_ship_size > 5:
            return 1
        
        return smallest_ship_size

    def update_parity(self, enemy_board):
        """
        Checks if the parity jump distance needs to change.
        
        Get the current smallest alive ship size using the helper above.
        Check if this size is different from self.parity.
        If it is different, update self.parity to the new size and set self.needs_recalc to True.
        """
        curr_parity = self._get_smallest_alive_ship(enemy_board)

        if curr_parity != self.parity:
            self.parity = curr_parity
            self.needs_recalc=True

    def calc_scores(self, enemy_board):
        """
        Performs the full Dynamic Parity and Bridge Check scoring.
        
        Reset self.score_grid to all 0s.
        Loop through every row (0-9) and col (0-9).
        Skip the cell if it is NOT a parity square: (row + col) % self.parity != 0.
        Skip the cell if it has already been shot at (check self.shots_fired).
        For valid parity squares, check its 4 orthogonal directions (N, S, E, W).
        Check the "bridges" (spaces between the current cell and the jump distance).
        If all bridge spaces are un-hit water AND the destination square (at jump distance) is un-hit water, add +1 to this square's score in self.score_grid.
        Set self.needs_recalc to False.
        """
        def check(r,c):
            if 0<=r<10 and 0<=c<10 and enemy_board.grid[r][c] not in (HIT,MISS):
                return 1
            return 0
            
        self.score_grid = [[0 for i in range(10)] for i in range(10)]
        for row in range(10):
            for col in range(10):
                if (row+col) % self.parity == 0:
                    self.score_grid[row][col]+=(
                        all(check(row+i,col) for i in range(1,self.parity))+
                        all(check(row,col+i) for i in range(1,self.parity))+
                        all(check(row-i,col) for i in range(1,self.parity))+
                        all(check(row,col-i) for i in range(1,self.parity))
                        )
        
        self.needs_recalc=False
                    
    def patch_scores(self, row, col):
        # HarishWasHere
        """
        The Smart Cache: Locally downgrades scores around a Miss.
        
        Set self.score_grid[row][col] to 0.
        Calculate the coordinates of the 4 parity neighbors (distance = self.parity).
        For each neighbor, if it is within the 10x10 board boundaries, subtract 1 from its score in self.score_grid (ensure it doesn't go below 0).
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
        
        Find the maximum score currently in self.score_grid (excluding already shot coords).
        Collect all (row, col) tuples that have this maximum score into a list.
        If the list is empty (edge case when board is extremely full), return a random un-shot coordinate.
        Otherwise, return a random choice from your list of best moves.
        """

        # Not fully done yet
        # HarishWasHereToo
        max_score = max([max(row_score) for row_score in self.score_grid])
        max_score_tuples = []

        for row in range(10):
            for col in range(10):
                if self.score_grid[row][col] == max_score and (row,col) not in self.shots_fired:
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
        
        Loop while self.target_stack is not empty.
        Pop a coordinate (row, col) from the stack.
        If it is NOT in self.shots_fired, return it.
        If the loop finishes and nothing was returned (stack ran dry), set self.hunting = True and return self.hunt().
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
        
        Call self.update_parity(enemy_board). If self.needs_recalc is True, call self.calc_scores(enemy_board).
        If self.hunting is True, get (row, col) from self.hunt(). Else, get (row, col) from self.target().
        Call enemy_board.receive_attack(row, col) and add (row, col) to self.shots_fired.
        Print a message showing where the AI fired and what the result was.
        React to Result:
        If result is "MISS" and self.hunting is True -> call self.patch_scores(row, col).
        If result is "HIT" -> set self.hunting to False. Add the 4 immediate orthogonal valid neighbors (distance 1) to self.target_stack.
        If result is "SUNK" -> set self.hunting to True, clear the target_stack, and set self.needs_recalc to True.
        Return the result string.
        """

        #Helper function
        def check(r,c):
            if 0<=r<10 and 0<=c<10 and enemy_board.grid[r][c] not in (HIT,MISS):
                return 1
            return 0


        self.update_parity(enemy_board)

        if self.needs_recalc:
            self.calc_scores(enemy_board)

        if self.hunting:
            row, col = self.hunt()
        else:
            row, col = self.target()

        res = enemy_board.receive_attack(row, col)
        self.shots_fired.add((row, col))

        print("AI fired at ", row, ", ", col, " and the result was ", res)

        match res:
            case "MISS":
                if self.hunting:
                    self.patch_scores(row, col)
            case "HIT":
                self.hunting = False
                if not self.start:
                    targets = [(row+1, col), (row, col-1), (row-1, col), (row,col+1)]
                    self.start = (row,col)
                else:
                    if row==self.start[0]:
                        targets = [(row,col-1), (row, col+1)]
                    else:
                        targets=[(row-1, col), (row+1, col)]

                for i,j in targets:
                    if check(i,j):
                        self.target_stack.append((i,j))

            case "SUNK":
                self.hunting = True
                self.target_stack = []
                self.needs_recalc = True
                self.start=None

        return result




    
        
       
