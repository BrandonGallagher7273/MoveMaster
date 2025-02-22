import unittest
from generator import *

class TestJengaTower(unittest.TestCase):
    def setUp(self):
        self.tower = Tower("TestTower")
    
    def test_initial_tower_valid(self):
        # Test if the initial tower state is valid.
        self.assertTrue(self.tower.isTowerValid())
    
    def test_single_move_valid(self):
        # Move a single block and ensure validity remains.
        self.tower.move(10, 2)
        self.assertTrue(self.tower.isTowerValid())
    
    def test_tower_collapse(self):
        # Simulate moves until the tower collapses.
        sequence = self.tower.generateSequence()
        self.assertFalse(self.tower.isTowerValid())
    
    def test_max_layers(self):
      # Ensure validity with exactly 52 layers.
      seq = "1.1 4.2 7.3 10.1 13.2 16.3 19.1 22.2 25.3 28.1 31.2 34.3 37.1 40.2 43.3 46.1 49.2 52.3 3.1 6.2 9.3 12.1 15.2 18.3 21.1 24.2 27.3 30.1 33.2 36.3 39.1 42.2 45.3 48.1 51.2 54.3 1.1 10.2 19.3 28.1 37.2 46.3 3.1 12.2 21.3 30.1 39.2 7.3 16.1 25.2 34.3 43.1 52.2 9.3 18.1 27.2 36.3 45.1 48.2 1.3 28.1 3.2 30.3 16.1 43.2 18.3 54.1 19.2 46.3 21.1 7.2 34.3 9.1 36.2 45.3 28.1 16.2 54.3 21.1 1.2 30.3 18.1 46.2 34.3 9.1 28.2 21.3 45.1 54.2 30.3 18.1 9.2 34.3 21.1 45.2 18.3 30.1 34.2 21.3 18.1 30.2 21.3"
      seqSplit = seq.split()
      for i,move in enumerate(seqSplit):
         seqSplit[i] = move.split(".")

      for move in seqSplit:
         self.tower.move(int(move[0]),int(move[1]))

      self.assertTrue(self.tower.isTowerValid())
    
    def test_too_many_layers(self):
      # Adding a 53rd layer should make isTowerValid return False.
      seq = "1.1 4.2 7.3 10.1 13.2 16.3 19.1 22.2 25.3 28.1 31.2 34.3 37.1 40.2 43.3 46.1 49.2 52.3 3.1 6.2 9.3 12.1 15.2 18.3 21.1 24.2 27.3 30.1 33.2 36.3 39.1 42.2 45.3 48.1 51.2 54.3 1.1 10.2 19.3 28.1 37.2 46.3 3.1 12.2 21.3 30.1 39.2 7.3 16.1 25.2 34.3 43.1 52.2 9.3 18.1 27.2 36.3 45.1 48.2 1.3 28.1 3.2 30.3 16.1 43.2 18.3 54.1 19.2 46.3 21.1 7.2 34.3 9.1 36.2 45.3 28.1 16.2 54.3 21.1 1.2 30.3 18.1 46.2 34.3 9.1 28.2 21.3 45.1 54.2 30.3 18.1 9.2 34.3 21.1 45.2 18.3 30.1 34.2 21.3 18.1 30.2 21.3 2.1"
      seqSplit = seq.split()
      for i,move in enumerate(seqSplit):
         seqSplit[i] = move.split(".")
      for move in seqSplit:
         self.tower.move(int(move[0]),int(move[1]))

      self.assertFalse(self.tower.isTowerValid())
    
    def test_duplicate_block_id(self):
        # Ensure tower is invalid if duplicate block IDs exist.
        self.tower.tower[0][0].setID(5)
        self.assertFalse(self.tower.isTowerValid())
    
    def test_out_of_bounds_block_id(self):
        # Ensure invalid tower if a block ID is out of range (e.g., 55).
        self.tower.tower[0][0].setID(55)
        self.assertFalse(self.tower.isTowerValid())
    
    def test_consecutive_null_blocks(self):
        # Ensure tower is invalid if two consecutive null blocks exist.
        self.tower.tower[0][0].setID(-1)
        self.tower.tower[0][1].setID(-1)
        self.assertFalse(self.tower.isTowerValid())
    
    def test_random_valid_sequence(self):
        # Test a generated sequence and ensure its validity.
        sequence = self.tower.generateSequence()
        self.assertTrue(isValidSequence(sequence))
    
    def test_top_layer_occupied_spot(self):
        # Ensure moving a block to an already occupied top layer spot is invalid.
        self.tower.move(5, 1)
        self.tower.move(10, 1)  # Should fail since position 1 is already taken
        self.assertFalse(self.tower.isTowerValid())
    
    def test_block_removed_not_placed(self):
        # If a block is removed and not placed back, tower should be invalid.
        self.tower.tower[0][0].setID(-1)  # Remove a block without adding it to the top
        self.assertFalse(self.tower.isTowerValid())
    
if __name__ == "__main__":
    unittest.main()
