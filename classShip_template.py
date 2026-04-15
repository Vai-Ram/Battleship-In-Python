class Ship:
    """
    A class representing a single ship in the game.
    It tracks its own size, location, and damage status.
    """

    def __init__(self, name, size):
        """
        Initialize the Ship object.
        """
        self.name = name
        self.size = size
        self.coordinates = [] # Stores (row, col) tuples. Populated by Board.place_ship()
        self.hits = 0         # specific hit counter for this ship

    def record_hit(self):
        """
        Registers damage to the ship when one of its coordinates is hit.
        """
        self.hits += 1

    def is_sunk(self):
        """
        Checks if the ship is destroyed.
        """
        return self.hits >= self.size
