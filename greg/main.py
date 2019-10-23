import os
import sys
import time

from Papashcode.random_builder import random_solution
from Papashcode.utils import load_file, rateFile, write_solution, extract_data


def test_evaluator(fileName):
    inPath = "./data/" + fileName + ".in"
    outPath = "./data/" + fileName + ".out"
    with open(inPath) as i:
        sys.stdin = i
        print(load_file())
    print(rateFile(outPath, inPath))
def runner(function):
    home_path = "./data"
    for file in os.listdir(home_path):
        if "in" in file:
            print(file)
            outputPath = home_path+"/"+file.replace(".in",str(time.time())+".out")
            input_path = home_path +"/"+ file
            write_solution(function(input_path), outputPath)

            print(rateFile(outputPath, input_path))

if __name__ == '__main__':
    runner(lambda x:random_solution(extract_data(x)))


