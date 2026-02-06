# Constants for cell states
WATER = "~"
SHIP  = "S"
MISS  = "O"
HIT   = "X"

class Board:
    def __init__(self, size=10):
        """
        Initialize the board.
        1. Set self.size to size (default 10).
        2. Create self.grid: a 10x10 list of lists filled with WATER.
        3. Create self.ships: an empty list to track Ship objects.
        """
        pass

    def place_ship(self, ship, start_row, start_col, orientation):
        """
        Attempts to place a ship on the board.
        
        Logic to implement:
        1. Bounds Check: Ensure the ship doesn't go off the edge (index > 9).
        2. Overlap Check: Ensure every cell the ship takes is currently WATER.
        3. If valid: Update grid cells to SHIP, update ship.coordinates, add to self.ships.
        
        Returns: True if placed successfully, False if invalid.
        """
        pass

    def receive_attack(self, row, col):
        """
        Processes an incoming shot at (row, col).
        
        Logic to implement:
        1. Check Bounds: Return "INVALID" if row/col is not 0-9.
        2. Check Duplicates: Return "DUPLICATE" if cell is already HIT or MISS.
        3. If WATER: Mark as MISS, return "MISS".
        4. If SHIP: Mark as HIT, find the ship object, call ship.record_hit().
           - If ship.is_sunk() is True, return "SUNK".
           - Else return "HIT".
        """
        pass

    def all_ships_sunk(self):
        """
        Checks if the game is over.
        
        Logic to implement:
        - Return True if ALL ships in self.ships are sunk.
        - Return False otherwise.
        """
        pass

    def display(self, hide_ships=False):
        """
        Prints the board grid to the console.
        
        Logic to implement:
        - Print column numbers (1-10) at the top.
        - Loop through rows, printing the Row Letter (A-J) then the cells.
        - If hide_ships=True: Print WATER instead of SHIP (to hide them).
        - Always show HIT and MISS markers.
        """
        pass