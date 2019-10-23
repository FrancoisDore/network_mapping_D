from compute import *
from utils import *
import os

path_to_datasets = "data"

functions = [
    ("Random", random_solution),
    ("Spiral", spiral_solution),
    ("Greedy (rdm)", lambda x: greedy_solution(x, mode="random")),
    ("Greedy (deg)", lambda x: greedy_solution(x, mode="degree")),
    ("Greedy (ngh)", lambda x: greedy_solution(x, mode="neighbours"))
]
initials = functions[:]
functions += [
    ("Complete Swapper", lambda data: complete_swapper(data, initials=list(map(lambda t: t[1], initials)))),
    ("Random Swapper", lambda data: random_swaper(data, initials=list(map(lambda t: t[1], initials)))),
    ("Greeddy Mover", lambda data: greedy_mover(data, initials=list(map(lambda t: t[1], initials)))),
]
if __name__ == '__main__':
    files, results = sorted(os.listdir(path_to_datasets), key=lambda x: int(x.split(".")[0][2:])), []
    for filename in files:
        data = extract_data(path_to_datasets + "/" + filename)
        results.append(list(map(lambda f: evaluate_solution(data, f[1](data)), functions)))
    print_matrix(results, list(map(lambda x: x[0], functions)), files)
