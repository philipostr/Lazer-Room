import unittest
from unittest.mock import MagicMock, patch
import lazer_sim
from lazer_sim import *
#from mutpy import commandline
import sys

class Test(unittest.TestCase):

#TO TEST:
# smallest_vec
# generate_surroundings
# distance
# simulate

    #Unit tests for smallest_vec method
    def test_smallest_vec_pass(self):
        self.assertEqual(smallest_vec([2,2]),(1,1))

    @unittest.expectedFailure
    def test_smallest_vec_fail(self):
        self.assertEqual(smallest_vec([2,6]),(2,3))

    #CHANGE: needed to convert return value in code from a list to a tuple
    def test_smallest_vec_zero(self):
        self.assertEqual(smallest_vec([0,0]),(0,0))

    #Unit tests for distance method
    def test_distance_pass(self):
        self.assertEqual(distance([5,6],[-7,11]),13)

    @unittest.expectedFailure
    def test_distance_fail(self):
        self.assertEqual(distance([8,6]),9)

    #Unit tests for generate_surroundings method
    def test_generate_surroundings_origin_room(self):
        og_room = { 'inc': (1,1), 'tar': (2,1), 'xflip': False, 'yflip': False }
        self.assertEqual(generate_surroundings(og_room, og_room, 3, 3), [
            { 'inc': (1, 5), 'tar': (2, 5), 'xflip': False, 'yflip': True }, #up
            { 'inc': (5, 1), 'tar': (4, 1), 'xflip': True, 'yflip': False }, #right
            { 'inc': (1, -1), 'tar': (2, -1), 'xflip': False, 'yflip': True }, #down
            { 'inc': (-1, 1), 'tar': (-2, 1), 'xflip': True, 'yflip': False } #left
        ])

    def test_generate_surroundings_up_room(self):
        og_room = { 'inc': (1,1), 'tar': (2,1), 'xflip': False, 'yflip': False }
        up_room = { 'inc': (1, 5), 'tar': (2, 5), 'xflip': False, 'yflip': True }
        self.assertEqual(generate_surroundings(og_room, up_room, 3, 3), [
            { 'inc': (1, 7), 'tar': (2, 7), 'xflip': False, 'yflip': False }, #up
            { 'inc': (5, 5), 'tar': (4, 5), 'xflip': True, 'yflip': True }, #right
            { 'inc': (1, 1), 'tar': (2, 1), 'xflip': False, 'yflip': False }, #down
            { 'inc': (-1, 5), 'tar': (-2, 5), 'xflip': True, 'yflip': True } #left
        ])

    #CHANGE: Added to increase line coverage (if block was never being entered)
    def test_generate_surroundings_right_room(self):
        og_room = { 'inc': (1,1), 'tar': (2,1), 'xflip': False, 'yflip': False }
        right_room = { 'inc': (5, 1), 'tar': (4, 1), 'xflip': True, 'yflip': False }
        self.assertEqual(generate_surroundings(og_room, right_room, 3, 3), [
            { 'inc': (5, 5), 'tar': (4, 5), 'xflip': True, 'yflip': True }, #up
            { 'inc': (7, 1), 'tar': (8, 1), 'xflip': False, 'yflip': False }, #right
            { 'inc': (5, -1), 'tar': (4, -1), 'xflip': True, 'yflip': True }, #down
            { 'inc': (1, 1), 'tar': (2, 1), 'xflip': False, 'yflip': False } #left
        ])

    def test_generate_surroundings_no_dimensions(self):
        og_room = { 'inc': (0,0), 'tar': (0,0), 'xflip': False, 'yflip': False }
        self.assertEqual(generate_surroundings(og_room, og_room, 0, 0), [
            { 'inc': (0, 0), 'tar': (0, 0), 'xflip': False, 'yflip': True }, #up
            { 'inc': (0, 0), 'tar': (0, 0), 'xflip': True, 'yflip': False }, #right
            { 'inc': (0, 0), 'tar': (0, 0), 'xflip': False, 'yflip': True }, #down
            { 'inc': (0, 0), 'tar': (0, 0), 'xflip': True, 'yflip': False } #left
        ])

    #Unit tests for simulate method
    @patch('lazer_sim.generate_surroundings')
    def test_simulate_trivial(self, mock_generate):
        self.assertEqual(simulate(3, 3, (1, 1), (2, 1), 0, False), [(1, 0, 0)])
        mock_generate.assert_not_called()

    @patch('lazer_sim.generate_surroundings')
    def test_simulate_horizontal(self, mock_generate):
        without_pass_through = simulate(3, 3, (1, 1), (2, 1), 2, False)
        with_pass_through = simulate(3, 3, (1, 1), (2, 1), 2, True)
        self.assertEqual(without_pass_through, [
            (1, 0, 0), (1, 4, 1), (1, -2, 1), (1, 6, 2), (3, 4, 2), (-3, 4, 2),
            (3, -2, 2), (1, -6, 2), (-3, -2, 2)
        ])
        self.assertEqual(len(with_pass_through), len(without_pass_through)+1)

    @patch('lazer_sim.generate_surroundings')
    def test_simulate_vertical(self, mock_generate):
        pass

    @patch('lazer_sim.generate_surroundings')
    def test_simulate_angled(self, mock_generate):
        pass

if __name__ == '__main__':
    __spec__ = None
    unittest.main()
    #commandline.main(sys.argv)