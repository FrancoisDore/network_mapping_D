from collections import defaultdict, Counter
import operator


def extract_data(filename):
    """
    From the file given in input, generate the structure of the graph under the form of a dictionary which links a node
    to a list of all his neighbours
    """
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
    """
    Print a graph structure
    """
    for i in range(len(data)):
        print("{}: {}".format(i, data[i]))


def print_matrix(data, xlabels, ylabels):
    """
    Display a matrix as tabular data
    """
    row_format = "{:>15}" * (len(xlabels) + 1)
    print(row_format.format("", *xlabels))
    for team, row in zip(ylabels, data):
        print(row_format.format(team, *row))


def is_valid(data, solution):
    """
    Return True if a solution is valid given a graph structure, False otherwise
    """
    return not any([solution[i1] == solution[i2] for i1 in data for i2 in data[i1] if i2 > i1]) \
           and len(data) == len(solution)


def dist(c1, c2):
    """
    Compute the euclidean distance of two coordinates given under the of two tuples
    """
    return abs(c1[0] - c2[0]) + abs(c1[1] - c2[1])


def vertices_by_encounters(data):
    """
    Return a list of all the nodes of the graph
    Vertices are sorted by both connectivity and degree
    """
    res = []
    vertices = sorted(data.keys(), key=lambda x: -len(data[x]))
    for v in vertices:
        if v in res:
            continue
        nodes = [v]
        # We iterate on a list while extending it, this is bad
        # Don't try this at home, it's done by professionals
        for n in nodes:
            for nn in sorted(data[n], key=lambda x: -len(data[x])):
                if nn not in nodes:
                    nodes.append(nn)
        res.extend(nodes)
    return res


def format_solution(solution):
    """
    Given a solution under the form of a dictionary return, translate it to positive coordinates and format it in a list
    """
    min_x, min_y = [min(s[c] for s in solution.values()) for c in range(2)]
    return [tuple(map(operator.sub, solution[i], (min_x, min_y))) for i in range(len(solution))]


def evaluate_partial_solution(data, solution):
    """
    Compute the deficit of a partial solution
    (given that the solution is partial, the variable solution is a dictionary and not a list)
    """
    w = max([max([s[c] for s in solution.values()]) - min([s[c] for s in solution.values()]) for c in range(2)]) ** 2
    e = sum([2 * ((dist(solution[i1], solution[i2]) - 1) ** 2) for i1 in data if i1 in solution for i2 in data[i1] if
             i2 in solution and i2 > i1])
    s = sum(list(map(lambda x: 3 * ((x - 1) ** 2), Counter(solution.values()).values())))
    return w + e + s


def evaluate_solution(data, solution):
    """
    Compute the total deficit of a solution
    :param data: the structure of our graph
    :param solution: a list of the coordinates of each vertices
    :return: the points obtained following the rules given in the subject
    """
    if not is_valid(data,solution):
        return float('inf')
    w = max([max(s[c] for s in solution) - min(s[c] for s in solution) for c in range(2)]) ** 2
    e = sum([2 * ((dist(solution[i1], solution[i2]) - 1) ** 2) for i1 in data for i2 in data[i1] if i2 > i1])
    s = sum(list(map(lambda x: 3 * ((x - 1) ** 2), Counter(solution).values())))

    return w + e + s
