from utils import *
from compute import *

import json
import time

time_per_bench = 0.1

n_vertex_min, n_vertex_max = 1, 11
n_edges_min, n_edges_max = 0, 11

functions = [
    ("Random", random_solution),
    ("Spiral", spiral_solution),
    ("Greedy (rdm)", lambda x: greedy_solution(x, mode="random")),
    ("Greedy (deg)", lambda x: greedy_solution(x, mode="degree")),
    ("Greedy (ngh+)", lambda x: greedy_solution(x, mode="neighbours+")),
    ("Greedy (ngh-)", lambda x: greedy_solution(x, mode="neighbours-")),
]


def mean(l):
    return sum(l) / len(l)


D = dict()

for n_vertex in [2 ** i for i in range(n_vertex_min, n_vertex_max)]:
    D_edges = dict()
    for n_edges in [2 ** i for i in range(n_edges_min, n_edges_max)]:
        D_functions = dict()
        if n_edges > (n_vertex * (n_vertex - 1)) / 2:
            D_functions = {function[0]: {"time": None, "score": None} for function in functions}
        else:
            for function in functions:
                print(f"\r{n_vertex} vertices | {n_edges} edges | {function[0]} function", end="")
                bench_start = time.perf_counter()
                times, scores = [], []
                while time.perf_counter() - bench_start < time_per_bench:
                    instance = generate_instance(n_vertex, n_edges)
                    start = time.perf_counter()
                    s = function[1](instance)
                    times.append(time.perf_counter() - start)
                    scores.append(evaluate_solution(instance, s))
                D_functions[function[0]] = {"time": mean(times), "score": mean(scores)}
        D_edges[n_edges] = D_functions
    D[n_vertex] = D_edges

with open("results/results.json", "w") as file:
    file.write(json.dumps(D))
