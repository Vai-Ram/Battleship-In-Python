# Constants for cell states
WATER = "~"
SHIP  = "S"
MISS  = "O"
HIT   = "X"

class Board:

    def __init__(self, size=10):

        """
        Initialize the board.
        """

        self.size = size
        self.grid = [[WATER for i in range(size)] for j in range(size)]
        self.ships = []

    def place_ship(self, ship, start_row, start_col, orientation):

        """
        Attempts to place a ship on the board.
        """

        # Valid Coordinate Check
        if not(0 <= start_row < self.size and 0 <= start_col < self.size):
            return False

        # Possible orientations - 'V' or 'H' (per the player template file)

        if orientation == 'H':
            # Bounds Check
            if start_col + ship.size > self.size:
                return False

            # Overlap Check
            for i in range(ship.size):
                if self.grid[start_row][start_col + i] != WATER:
                    return False
            
            # Updation
            for i in range(ship.size):
                self.grid[start_row][start_col + i] = SHIP
                ship.coordinates.append((start_row, start_col + i))

            self.ships.append(ship)
            return True

        elif orientation == 'V':

            # Bounds Check
            if start_row + ship.size > self.size:
                return False

            # Overlap Check
            for i in range(ship.size):
                if self.grid[start_row + i][start_col] != WATER:
                    return False
            
            # Updation
            for i in range(ship.size):
                self.grid[start_row + i][start_col] = SHIP
                ship.coordinates.append((start_row + i, start_col))

            self.ships.append(ship)
            return True

        else:

            # Invalid orientation case
            return False 
        
    def receive_attack(self, row, col):
        """
        Processes an incoming shot at (row, col).
        """

        # Bounds checking
        if not ( 0 <= row < self.size and 0 <= col < self.size):
            return "INVALID"
        
        # Duplicate checking
        if self.grid[row][col] == MISS or self.grid[row][col] == HIT:
            return "DUPLICATE"

        # Implementing the attack

        elif self.grid[row][col] == WATER:
            self.grid[row][col] = MISS
            return "MISS"

        elif self.grid[row][col] == SHIP:
            self.grid[row][col] = HIT
            coords = (row, col)

            for i in self.ships:
                if coords in i.coordinates:
                    i.record_hit()

                    if i.is_sunk():
                        return "SUNK"
                    else:
                        return "HIT"          

    def all_ships_sunk(self):
        """
        Checks if the game is over.
        
        Logic to implement:
        - Return True if ALL ships in self.ships are sunk.
        - Return False otherwise.
        """
        
        for i in self.ships:
            if not i.is_sunk():
                return False

        else:
            return True

    def display(self, hide_ships=False):
        """
        Prints the board grid to the console.
        """
        
        # Printing the column headers
        i = 1
        
        print (' ', end = ' ')
        while i<=self.size:
            print(i, end = ' ')
            i += 1

        print()

        start = ord("A") #Using ASCII values to iterarate from A to J

        for i in range(self.size):
            print(chr(start+i), end = ' ')

            for j in range(self.size):
                if not hide_ships:
                    print(self.grid[i][j], end = ' ')
                
                else:
                    val = self.grid[i][j]

                    # Replacing ship with water when hide_ships is True

                    if val == SHIP:
                        val = WATER
                    
                    print(val, end = ' ')
            
            print()
