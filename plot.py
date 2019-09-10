import matplotlib.pyplot as plt
import numpy as np
from ast import literal_eval
import math


def read_state_from_file(f):
    for i in range(0,100):
        for j in range(0,100):
            l = f.readline()
            t = literal_eval(l)  # casting string to tuple
            state[i][j] = t
    return state


def plot():
    for i in range(0,100):
        for j in range(0,100):
            theta[i][j] = math.acos(state[i][j][2]) / math.pi * 2 - 1   # revert cartesian to sphere coordinate
            if j != 99:
                print(theta[i][j], end='  ')
            else:
                print(theta[i][j])
    for j in range(100):
        t = [j for i in range(100)]
        t1 = [i for i in range(100)]
        plt.scatter(t1, t, c=theta[j], marker="s", s=4)
    plt.colorbar()
    plt.show()


theta = [[0 for i in range(0,100)] for j in range(0,100)]
state = [[0 for i in range(0,100)] for j in range(0,100)]
file = open("export.txt","r+")
read_state_from_file(file)

plot()