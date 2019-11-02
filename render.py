import matplotlib.pyplot as plt
import math
import argparse
import json


def export_data():
    with open("results/results.json", 'r') as file:
        return json.loads(file.read())


def compute_lin_coeff(X, Y):
    if len(X) != len(Y):
        raise ValueError("The two lists doesn't have the same length")
    ln = len(X)

    def moy(l):
        return sum(l) / len(l)

    Xl = [math.log2(i) for i in X]
    Yl = [math.log2(i) for i in Y]

    num = moy([Xl[i] * Yl[i] for i in range(ln)]) - moy(Xl) * moy(Yl)
    denum = moy([i ** 2 for i in Xl]) - moy(Xl) ** 2
    a = num / denum
    return (a, moy(Yl) - a * moy(Xl))


colors = ["b", "g", "r", "c", "m", "y", "k"]

data = export_data()
fixed_vertices = 128
fixed_edges = 128
min_bound = 5

functions = ["Random", "Spiral", "Greedy (rdm)", "Greedy (deg)", "Greedy (ngh+)", "Greedy (ngh-)"]


def get_scores_for_fixed_vertices(vertices, function):
    return [e[function] for e in data[str(vertices)].values()]


def get_scores_for_fixed_edges(edges, function):
    return [e[str(edges)][function] for e in data.values()]


for function in functions:
    extracted = get_scores_for_fixed_edges(fixed_edges, function)
    x = [2 ** i for i in range(len(extracted))]
    y = [None if None in i.values() else i["time"] * i["score"] for i in extracted]
    a, b = compute_lin_coeff(x[min_bound:], y[min_bound:])
    print(f"{function}: {a:.2f}x{b:.2f}")
    plt.loglog(x, y)

plt.legend(functions)
plt.title("time * score(vertex), edges=128")
plt.savefig("plots/time_score(vertex).png")
