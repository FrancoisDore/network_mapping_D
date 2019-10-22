from compute import *
from utils import *
import os

path_to_datasets = "data"

if __name__ == '__main__':
    files, results = os.listdir(path_to_datasets), []
    for filename in files:
        data = extract_data(path_to_datasets + "/" + filename)
        results.append(list(map(lambda x: evaluate_solution(data, x),
                                [
                                    random_solution(data),
                                    gluttonous_solution(data, mode="random"),
                                    gluttonous_solution(data, mode="degree"),
                                    gluttonous_solution(data, mode="neighbours"),
                                ])))
    print_matrix(results, ["Random","Glutton (rdm)","Glutton (deg)","Glutton (ngh)"],files)
