import matplotlib.pyplot as plt
import numpy as np
from ast import literal_eval
import math


def load_state_from_file(f, state):
    for i in range(0,100):
        for j in range(0,100):
            l = f.readline()
            t = literal_eval(l)  # casting string to tuple
            state[i][j] = t


def plot(state):
    phase = [[0 for i in range(0, 100)] for j in range(0, 100)]
    for i in range(0,100):
        for j in range(0,100):
            phase[i][j] = state[i][j][1][0] * 2 - 1  # revert cartesian to sphere coordinate
            if j != 99:
                print(phase[i][j], end='  ')
            else:
                print(phase[i][j])
    for j in range(100):
        x = [i for i in range(100)]
        y = [j for i in range(100)]
        plt.scatter(x, y, c=phase[j], marker="s", s=4)
    plt.colorbar()
    plt.savefig(file.name + ".png")
    plt.show()


if __name__ == "__main__":
    state = [[0 for i in range(0,100)] for j in range(0,100)]
    file = open("export 1.0 1.0 1.0 0.99.txt","r+")
    load_state_from_file(file,state)

    plot(state)

