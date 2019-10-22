from compute import *

# ========================================
path_to_datasets = "data"
filename = "simple.in"
resolution_algorithm = gluttonous_solution
# ========================================


if __name__ == '__main__':
    data1 = extract_data(path_to_datasets + "/" + filename)
    sol = resolution_algorithm(data1)
    print("Solution:")
    print(sol)
    print(f"Deficit = {evaluate_solution(data1, sol)}")
