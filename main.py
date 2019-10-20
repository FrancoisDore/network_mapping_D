from compute import *

if __name__ == '__main__':
    data1 = extract_data("data/simple.in")
    GS = gluttonous_solution(data1)
    print(GS)
    print(evaluate_solution(data1, GS))
