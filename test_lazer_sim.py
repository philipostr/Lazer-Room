import unittest
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

    #Unit tests for distance method
    def test_distance_pass(self):
        self.assertEqual(distance([5,6],[-7,11]),13)

    @unittest.expectedFailure
    def test_distance_fail(self):
        self.assertEqual(distance([8,6]),9)

if __name__ == '__main__':
    __spec__ = None
    unittest.main()
    #commandline.main(sys.argv)