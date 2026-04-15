from classBoard_template import Board
from classShip_template import Ship
import random

class Player:
    def __init__(self, name):
        """
        Initialize the Player.
        1. Store self.name (e.g., "Player 1", "Player 2").
        2. Create self.board = Board() (This is the player's own fleet).
        3. Create self.shots_fired = set() (Tracks coordinates this player has attacked).
        """
        self.name = name
        self.board = Board()
        self.shots_fired = set()

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
        fleet = {
            "Carrier": 5, "Battleship": 4, "Submarine": 3, "Cruiser": 3, "Destroyer": 2
        }
        alpha={0:"A",1:"B",2:"C",3:"D",4:"E",5:"F",6:"G",7:"H",8:"I",9:"J"}
        for ship in fleet:
            while True:
                row = random.randint(0, 9)
                col = random.randint(0, 9)
                orientation = random.choice(['H', 'V'])
                ship_to_place = Ship(ship, fleet[ship])

                if self.board.place_ship(ship_to_place, row, col, orientation):
                    print(
                        f"{ship} successfully placed at {alpha[row]+str(col+1)} with orientation {orientation}")
                    break

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
        fleet = {
            "Carrier": 5, "Battleship": 4, "Submarine": 3, "Cruiser": 3, "Destroyer": 2
        }

        for ship in fleet:
            self.board.display()

            while True:
                coordinate = input(
                    f"Start coordinate for {ship} (Eg. C4): ").strip()
                orientation = input("Orientation (H/V): ").strip()

                if len(orientation) == 1 and orientation.lower() in ('h', 'v'):
                    if 2 <= len(coordinate) <= 3:
                        row = coordinate[0]
                        col = coordinate[1:]

                        if ('a' <= row.lower() <= 'j') and col.isdigit():
                            row = ord(row.lower()) - ord('a')
                            col = int(col) - 1

                            if 0 <= col <= 9:
                                ship_to_place = Ship(ship, fleet[ship])

                                if self.board.place_ship(ship_to_place, row, col, orientation):
                                    print(
                                        f"{ship} successfully placed at {coordinate} with orientation {orientation}")
                                    break
                                else:
                                    print("Invalid ship placement")
                            else:
                                print("Invalid input")
                        else:
                            print("Invalid input")
                    else:
                        print("Invalid input")
                else:
                    print("Invalid input")

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
        while True:
            coordinate = input(
                f"{self.name}, enter target coordinate: ").strip()
            if 2 <= len(coordinate) <= 3:
                row = coordinate[0]
                col = coordinate[1:]

                if ('a' <= row.lower() <= 'j') and col.isdigit():
                    row = ord(row.lower()) - ord('a')
                    col = int(col) - 1

                    if 0 <= col <= 9:
                        if (row, col) in self.shots_fired:
                            print("You already shot there!")
                        else:
                            result = enemy_board.receive_attack(row, col)
                            self.shots_fired.add((row, col))
                            print(result)
                            return result
                    else:
                        print("Invalid input")
                else:
                    print("Invalid input")
            else:
                print("Invalid input")
