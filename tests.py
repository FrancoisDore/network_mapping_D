import random
import unittest

from utils import is_valid
from compute import *


def generate_instance(n_vertex, n_edges):
    """
    Generate an instance of our problem with n_vertex vertices and n_edges edges
    (The generated graph can have lonely nodes)
    """
    edge_list = [(n1, n2) for n1 in range(n_vertex) for n2 in range(n1, n_vertex)]
    random.shuffle(edge_list)
    edges = {n: [] for n in range(n_vertex)}
    for e in edge_list[:n_edges]:
        edges[e[0]].append(e[1])
        edges[e[1]].append(e[0])
    return edges


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
            s = gluttonous_solution(instance)
            self.assertTrue(is_valid(instance, s))

    def test_encounters(self):
        for _ in range(100):
            instance = generate_instance(100, 200)
            v = vertices_by_encounters(instance)
            # Test if our list of vertices has all the nodes of our graph one and only one time
            self.assertEqual(len(instance.keys()), len(set(v)))


if __name__ == '__main__':
    unittest.main()
