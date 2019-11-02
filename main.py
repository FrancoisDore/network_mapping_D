from compute import *
from utils import *
import os

path_to_dataset = "data"
max_length_for_opportunistic = 10000
max_length_for_quadratic = 100000

functions = [
    random_solution,
    spiral_solution,
    lambda x: greedy_solution(x, mode="random"),
    lambda x: greedy_solution(x, mode="degree"),
    lambda x: greedy_solution(x, mode="neighbours+"),
    lambda x: greedy_solution(x, mode="neighbours-")
]
builders = functions[3:]
functions += [
    lambda data: complete_swapper(data, initials=builders),
    lambda data: random_swaper(data, initials=builders),
    lambda data: greedy_mover(data, initials=builders),
]
if __name__ == '__main__':
    input_files = os.listdir(path_to_dataset)
    data_l = len(input_files)
    for i, filename in enumerate(input_files):
        print(f"\r{i}/{data_l}: {filename}", end="")
        data = extract_data(path_to_dataset + "/" + filename)
        size = len(data)
        if size < max_length_for_opportunistic:
            fs = functions[6:]
        elif size < max_length_for_quadratic:
            fs = functions[2:6]
        else:
            fs = functions[0:2]
        solutions = list(map(lambda f: f(data), fs))
        best_solution = min(solutions, key=lambda s: evaluate_solution(data, s))
        write_solution("Binome_D/" + filename.replace("in", "ans"), best_solution)
