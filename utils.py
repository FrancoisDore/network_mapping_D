from collections import defaultdict, Counter
import operator


def extract_data(filename):
    with open(filename, "r") as file:
        edges = defaultdict(set)
        data = file.read().split("\n")
        V, E = list(map(int, data[0].split(" ")))
        for i in range(1, E + 1):
            v1, v2 = list(map(int, data[i].split(" ")))
            edges[v1].add(v2)
            edges[v2].add(v1)
        return edges


def display_edges(data):
    for i in range(len(data)):
        print("{}: {}".format(i, data[i]))


def is_valid(data, solution):
    return not any([solution[i1] == solution[i2] for i1 in data for i2 in data[i1] if i2 > i1])


def dist(c1, c2):
    return abs(c1[0] - c2[0]) + abs(c1[1] - c2[1])


def format_solution(solution):
    min_x, min_y = [min(s[c] for s in solution.values()) for c in range(2)]
    return [tuple(map(operator.sub, solution[i], (min_x, min_y))) for i in range(len(solution))]


def evaluate_partial_solution(data, solution):
    w = max([max([s[c] for s in solution.values()]) - min([s[c] for s in solution.values()]) for c in range(2)]) ** 2
    e = sum([2 * ((dist(solution[i1], solution[i2]) - 1) ** 2) for i1 in data if i1 in solution for i2 in data[i1] if
             i2 in solution and i2 > i1])
    s = sum(list(map(lambda x: 3 * ((x - 1) ** 2), Counter(solution.values()).values())))
    return w + e + s


def evaluate_solution(data, solution):
    w = max([max(s[c] for s in solution) for c in range(2)]) ** 2
    e = sum([2 * ((dist(solution[i1], solution[i2]) - 1) ** 2) for i1 in data for i2 in data[i1] if i2 > i1])
    s = sum(list(map(lambda x: 3 * ((x - 1) ** 2), Counter(solution).values())))
    return w + e + s
