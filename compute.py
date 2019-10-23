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


def spiral_solution(data):
    """
    Place vertices in spiral according to their number of neighbours
    :param data: must be of the form {n : L, ...} with n a vertex and L the list of all the vertices adjacent to n
    :return: a list of the coordinates of each vertex
    """
    vertices = sorted(data.keys(), key=lambda x: -len(data[x]))
    res = [None] * len(data)
    dirs = [(1, 0), (0, -1), (-1, 0), (0, 1)]
    d, cpt, borne, toggle = 0, 0, 1, False
    l = ceil(sqrt(len(data)))
    x, y = (l - 1) // 2, l // 2
    for v in vertices:
        res[v] = (x, y)
        x, y = x + dirs[d][0], y + dirs[d][1]
        cpt += 1
        if cpt >= borne:
            borne += 1 if toggle else 0
            toggle = not toggle
            cpt = 0
            d = (d + 1) % 4
    return res


def greedy_solution(data, mode="neighbours"):
    """
    Offers a gluttonous solution:
    for each vertex ranked according to the mode:
        place it at a distance of maximum one case from another vertex in a way to minimize the deficit
    :param data: must be of the form {n : L, ...} with n a vertex and L the list of all the vertices adjacent to n
    :param mode: define the way to run through vertices
        - "random": run through vertices in a random order
        - "degree": prioritize vertices with a bigger degree
        - "neighbours": run through vertices by prioritizing firstly with connectivity then with the degree
    :return: a list of the coordinates of each vertex
    """

    # TODO mode avec les grands voisin pour trouver des facettes (cycles de 4)

    def expand(c):
        return {(c[0] + x, c[1] + y) for x, y in [(0, 1), (1, 0), (0, -1), (-1, 0)]}

    coords = dict()
    if mode == "degree":
        # Sort the vertices by their number of neighbours
        vertices = sorted(data.keys(), key=lambda x: -len(data[x]))
    elif mode == "random":
        # Even if the keys of a dictionary are not indexed, we shuffle them to be sure
        vertices = list(data.keys())
        random.shuffle(vertices)
    else:
        vertices = vertices_by_encounters(data)
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

