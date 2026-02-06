class Ship:
    def __init__(self, name, size):
        """
        Initialize the Ship.
        
        Logic to implement:
        1. Store self.name (e.g., "Destroyer").
        2. Store self.size (e.g., 2).
        3. Initialize self.coordinates = [] (Empty list to store (row, col) tuples later).
        4. Initialize self.hits = 0 (Tracks damage).
        """
        pass

    def record_hit(self):
        """
        Registers damage to the ship.
        
        Logic to implement:
        1. Increment self.hits by 1.
        """
        pass

    def is_sunk(self):
        """
        Checks if the ship is destroyed.
        
        Logic to implement:
        1. Return True if self.hits is equal to self.size.
        2. Otherwise, return False.
        """
        pass