import sys
from collections import Counter, defaultdict


def load_file():
    count = sys.stdin.readline()
    edges = set()
    for line in sys.stdin:
        edges.add(tuple(map(int,line.split())))
    return edges

def write_solution(solution,outputPath):
    with open(outputPath,"w") as outFile:
        for position in solution:
            outFile.write(" ".join(map(str,position))+"\n")

def extract_data(filename):
    with open(filename,"r") as file:
        edges=defaultdict(set)
        data=file.read().split("\n")
        V,E=list(map(int,data[0].split(" ")))
        for i in range(1,E):
            v1,v2=list(map(int,data[i].split(" ")))
            edges[v1].add(v2)
            edges[v2].add(v1)
        return edges
def distance(a,b):
    return abs(a[0]-b[0])+abs(a[1]-b[1])


def rateFile(solutionPath, inputPath):
    with open(inputPath) as inputFile:
        sys.stdin = inputFile
        probleme = load_file()
    with open(solutionPath) as solutionFile:
        solution = dict(enumerate(map(lambda x:tuple(map(int,x.split())),solutionFile)))
    edgePoints = 0

    for edge in probleme:
        positions = list(map(lambda x: solution[x], edge))
        # print(positions,":",distance(*positions))
        if len(set(positions))==1:
            return 0
        edgePoints+= 2 * ((distance(*positions) - 1) ** 2)

    maxX = max(map(lambda x:x[0],solution.values()))
    maxY = max(map(lambda x:x[1],solution.values()))
    superpositions = sum(map(lambda x:3*(x-1)**2,Counter(solution.values()).values()))
    size = max(maxX, maxY) ** 2
    print("sup",superpositions)
    print("size",size)
    print("edges",edgePoints)
    return superpositions + size + edgePoints


