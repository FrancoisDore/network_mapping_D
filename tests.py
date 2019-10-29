import random
import unittest

from utils import is_valid
from compute import *


class SolutionValidator(unittest.TestCase):

    def test_random_solutions(self):
        for _ in range(100):
            instance = generate_instance(100, 200)
            s = random_solution(instance)
            self.assertTrue(is_valid(instance, s))

    def test_pseudo_linear_solutions(self):
        for _ in range(100):
            instance = generate_instance(100, 200)
            s = spiral_solution(instance)
            self.assertTrue(is_valid(instance, s))

    def test_gluttonous_solutions(self):
        for _ in range(100):
            instance = generate_instance(100, 200)
            s = greedy_solution(instance)
            self.assertTrue(is_valid(instance, s))

    def test_encounters(self):
        for _ in range(100):
            instance = generate_instance(100, 200)
            v = vertices_by_encounters(instance)
            # Test if our list of vertices has all the nodes of our graph one and only one time
            self.assertEqual(len(instance.keys()), len(set(v)))


if __name__ == '__main__':
    unittest.main()
