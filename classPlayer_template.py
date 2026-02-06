class Player:
    def __init__(self, name):
        """
        Initialize the Player.
        1. Store self.name (e.g., "Player 1", "Player 2").
        2. Create self.board = Board() (This is the player's own fleet).
        3. Create self.shots_fired = set() (Tracks coordinates this player has attacked).
        """
        pass

    def random_place_ships(self):
        """
        Auto-Placement Logic: Randomly places the standard fleet on self.board.
        1. Define fleet sizes: [5, 4, 3, 3, 2].
        2. Loop through each size:
           - Loop continuously (retry mechanism):
             - Generate random row (0-9), col (0-9), and orientation ('H'/'V').
             - Create a Ship object.
             - Call self.board.place_ship(...).
             - If True: Break retry loop, move to next ship size.
             - If False: Continue retry loop (position was invalid).
        """
        pass

    def manual_place_ships(self):
        """
        Manual Placement Logic: Guides the user to place ships via the terminal.
        1. Define fleet: [("Carrier", 5), ("Battleship", 4), ("Cruiser", 3), ("Sub", 3), ("Destroyer", 2)].
        2. Loop through each ship in the fleet:
           - Call self.board.display() to show current board state.
           - Loop continuously (input validation):
             - Prompt user for Coordinate (e.g., "A1") and Orientation (e.g., "H").
             - Convert input to (row, col).
             - Create a Ship object.
             - Call self.board.place_ship(...).
             - If True: Print success message, break validation loop.
             - If False: Print error ("Invalid/Overlap"), repeat validation loop.
        """
        pass

    def attack(self, enemy_board):
        """
        Executes a turn against the opponent.
        1. Loop continuously (to ensure valid input):
           - Prompt user: f"{self.name}, enter target coordinate: "
           - Convert input to (row, col).
           - Check if (row, col) is in self.shots_fired.
             - If yes: Print "You already shot there!", repeat loop.
             - If no: Break loop.
        2. Call enemy_board.receive_attack(row, col).
        3. Add (row, col) to self.shots_fired.
        4. Print the result (e.g., "Hit!", "Miss!", "Sunk!").
        5. Return the result string.
        """
        pass