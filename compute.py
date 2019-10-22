from utils import *
from math import ceil, sqrt
import random


def random_solution(data):
    """
    Offers a random valid solution to the network cartography problem
    :param data: must be of the form {n : L, ...} with n a vertex and L the list of all the vertices adjacent to n
    :return: a list of the coordinates of each vertex
    """

    len_min_square = ceil(sqrt(len(data)))
    L = list(range(len_min_square ** 2))
    random.shuffle(L)
    return [(L[i] // len_min_square, L[i] % len_min_square) for i in range(len(data))]


def gluttonous_solution(data, mode="degree"):
    """
    Offers a gluttonous solution:
    for each vertex ranked by the number of theirs neighbours:
        place it at a distance of maximum on case from another vertex in a way to minimize the deficit
    :param data: must be of the form {n : L, ...} with n a vertex and L the list of all the vertices adjacent to n
    :return: a list of the coordinates of each vertex
    """

    def expand(c):
        return {(c[0] + x, c[1] + y) for x, y in [(0, 1), (1, 0), (0, -1), (-1, 0)]}

    coords = dict()
    if mode == "neighbours":
        #
        vertices = vertices_by_encounters(data)
    elif mode == "random":
        # Even if the keys of a dictionary are not indexed, we shuffle them to be sure
        vertices = list(data.keys())
        random.shuffle(vertices)
    else:
        # Sort the vertices by their number of neighbours
        vertices = sorted(data.keys(), key=lambda x: -len(data[x]))
    solution, possibilities = {vertices[0]: (0, 0)}, {(0, 0)}
    possibilities.update(expand((0, 0)))
    for node in vertices[1:]:
        deficit, coord = None, None
        for p in possibilities:
            # Prohibit coordinates where one of his neighbour already is
            if p in map(lambda x: solution[x], filter(lambda x: x in solution, data[node])):
                continue
            solution[node] = p
            d = evaluate_partial_solution(data, solution)
            if deficit is None or d < deficit:
                deficit, coord = d, p
        solution[node] = coord
        possibilities.update(expand(coord))
    return format_solution(solution)
