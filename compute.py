from tqdm import tqdm

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


def gluttonous_solution(data, mode="neighbours"):
    """
    Offers a gluttonous solution:
    for each vertex ranked according to the mode:
        place it at a distance of maximum one case from another vertex in a way to minimize the deficit
    :param data: must be of the form {n : L, ...} with n a vertex and L the list of all the vertices adjacent to n
    :return: a list of the coordinates of each vertex
    """

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


def bogo_randomizer(data, initial):
    first_round = initial(data)
    score = evaluate_solution(data, first_round)
    bogo_score = score
    bogo = first_round[:]
    while bogo_score >= score:
        random.shuffle(bogo)
        bogo_score = evaluate_solution(data, bogo)
    return bogo


def swap_in_place(index_a, index_b, data):
    data[index_a],data[index_b] = data[index_b],data[index_a]

def complete_swapper(data, initials):
    first_round, score = select_best(data, initials)
    score = evaluate_solution(data, first_round)
    solution = first_round[:]
    for i in range(len(first_round)):
        for j in range(i + 1, len(first_round)):
            swap_in_place(i, j, solution)
            if score < evaluate_solution(data, solution):
                swap_in_place(i, j, solution)
    return solution


def random_swaper(data, initials):
    first_round, score = select_best(data, initials)
    order = list(range(len(first_round)))
    solution = first_round
    for i in range(10000):
        random.shuffle(order)
        work_in_progress = first_round[:]
        for i in range(len(first_round)):
            swap = order[i]
            swap_in_place(i, swap, work_in_progress)
            if score < evaluate_solution(data, work_in_progress):
                swap_in_place(swap, i, work_in_progress)
        if score >= evaluate_solution(data, work_in_progress):
            solution = work_in_progress
    return work_in_progress


def select_best(data, algorithms):
    """Take an array of lambda(data)->result
        returns the best result and score produced in the array for the passed dataset"""
    score = float('inf')
    best_result = []
    for initial in algorithms:
        candidate = initial(data)
        candidate_score = evaluate_solution(data, candidate)
        if score > candidate_score:
            score = candidate_score
            best_result = candidate
    return best_result, score


def greedy_mover(data, initials):
    first_round, score = select_best(data, initials)
    possibilities = set(first_round)
    def neightbours(point):
        dirs = [(0,1),(1,0),(-1,0),(0,-1)]
        return tuple(map(lambda d:(tuple(map(sum,zip(point,d)))),dirs))
    for i in first_round:
        for n in neightbours(i):possibilities.add(n)
    for i in range(len(first_round)):
        for p in possibilities:
            prev, first_round[i] = first_round[i], p
            if score < evaluate_solution(data,first_round):
                first_round[i] = prev
    return first_round