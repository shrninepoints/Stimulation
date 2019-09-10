import matplotlib.pyplot as plt
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
    theta = [[0 for i in range(0,100)] for j in range(0,100)]
    for i in range(0,100):
        for j in range(0,100):
            theta[i][j] = math.acos(state[i][j][2])   # revert cartesian to sphere coordinate
            if j != 99:
                print(theta[i][j] / math.pi - 1, end='  ')
            else:
                print(theta[i][j])



state = [[0 for i in range(0,100)] for j in range(0,100)]
file = open("export.txt","r+")
read_state_from_file(file)

plot()

