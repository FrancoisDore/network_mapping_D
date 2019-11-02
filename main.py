from compute import *
from utils import *
import os

path_to_dataset = "data"
s_opportunistic = 5000
s_quadratic = 100000

functions = [
    (float("inf"), random_solution),
    (float("inf"), spiral_solution),
    (s_quadratic, lambda x: greedy_solution(x, mode="random")),
    (s_quadratic, lambda x: greedy_solution(x, mode="degree")),
    (s_quadratic, lambda x: greedy_solution(x, mode="neighbours+")),
    (s_quadratic, lambda x: greedy_solution(x, mode="neighbours-"))
]
builders = functions[3:]
functions += [
    (s_opportunistic, lambda data: complete_swapper(data, initials=list(map(lambda t: t[1], builders)))),
    (s_opportunistic, lambda data: random_swaper(data, initials=list(map(lambda t: t[1], builders)))),
    (s_opportunistic, lambda data: greedy_mover(data, initials=list(map(lambda t: t[1], builders)))),
]
if __name__ == '__main__':
    input_files = os.listdir(path_to_dataset)
    data_l = len(input_files)
    for i, filename in enumerate(input_files):
        print(f"\r{i+1}/{data_l}: {filename}", end="")
        data = extract_data(path_to_dataset + "/" + filename)
        size = len(data)
        fs = [f[1] for f in functions if f[0] >= size]
        solutions = list(map(lambda f: f(data), fs))
        best_solution = min(solutions, key=lambda s: evaluate_solution(data, s))
        write_solution("Binome_D/" + filename.replace("in", "ans"), best_solution)
