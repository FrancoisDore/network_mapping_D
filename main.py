from compute import *
from utils import *

# ========================================
path_to_datasets = "data"
filename = "TR36.in"
resolution_algorithm = gluttonous_solution
# ========================================


if __name__ == '__main__':
    data1 = extract_data(path_to_datasets + "/" + filename)
    for mode in ["random", "degree", "neighbours"]:
        sol = resolution_algorithm(data1, mode=mode)
        print(f"Deficit (mode={mode}) = {evaluate_solution(data1, sol)}")
