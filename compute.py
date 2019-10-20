from utils import *
from math import ceil, sqrt
import random


def random_solution(data):
    len_min_square = ceil(sqrt(len(data)))
    L = list(range(len_min_square ** 2))
    random.shuffle(L)
    return [(L[i] // len_min_square, L[i] % len_min_square) for i in range(len(data))]


def gluttonous_solution(data):
    def expand(c):
        return {(c[0] + x, c[1] + y) for x, y in [(0, 1), (1, 0), (0, -1), (-1, 0)]}

    coords, rkd = dict(), sorted(data.keys(), key=lambda x: -len(data[x]))
    solution, possibilities = {rkd[0]: (0, 0)}, {(0, 0)}
    possibilities.update(expand((0, 0)))
    for node in rkd[1:]:
        deficit, coord = None, None
        for p in possibilities:
            if p in map(lambda x: solution[x], filter(lambda x: x in solution, data[node])):
                continue
            solution[node] = p
            d = evaluate_partial_solution(data, solution)
            if deficit is None or d < deficit:
                deficit, coord = d, p
        solution[node] = coord
        possibilities.update(expand(coord))
    return format_solution(solution)
