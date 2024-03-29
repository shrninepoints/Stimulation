"""

The variable "state" is a 100 * 100 list, with each entry a tuple of tuple of float,
in the form of ((x, y, z), (theta / pi, phi / pi)).

The program will import "export G W.txt" as initial state from the current directory,
and will overwrite the file with the new state when the program terminate, if the
file exists. Else it will create such a file.

"""

import random
import math
import numpy as np
import matplotlib.pyplot as plt
import sys, getopt
from ast import literal_eval
import time


def random_vector():
    tupSphere = (random.random(), random.random() * 2)  # (theta,phi)
    tupCartesian = (math.sin(tupSphere[0] * math.pi) * math.cos(tupSphere[1] * math.pi),
                    math.sin(tupSphere[0] * math.pi) * math.sin(tupSphere[1] * math.pi),
                    math.cos(tupSphere[0] * math.pi))  # (x,y,z)
    return (tupCartesian, tupSphere)


def hamiltonian_local(m, n, vector):  # energy based on environment
    term1: float = np.dot(vector, state[(m + 1) % 100][n][0]) + \
                   np.dot(vector, state[(m - 1) % 100][n][0]) + \
                   np.dot(vector, state[m][(n - 1) % 100][0]) + \
                   np.dot(vector, state[m][(n + 1) % 100][0])
    term2: float = paraG * vector[2] * vector[2]
    term3: float = h[m][n] * vector[2]
    energy: float = - term1 / 2 - term2 + term3
    return energy


def hamiltonian_global():
    energy: float = 0
    for i in range(0, 100):
        for j in range(0, 100):
            energy += hamiltonian_local(i,j, state[i][j][0])
    return energy


def local_update(m, n, temperature):  # get a position (m,n), and accept or reject a randomVector result
    newVector = random_vector()
    deltaE = hamiltonian_local(m, n, newVector[0]) - hamiltonian_local(m, n, state[m][n][0])
    if deltaE < 0:
        state[m][n] = newVector
    else:
        acceptProbability = np.exp(-deltaE / temperature)
        if random.random() < acceptProbability:
            state[m][n] = newVector  # else the state do not change


def calculate(G, W, init_temp, temp_min):
    paraG = G
    paraW = W
    temperature = init_temp
    for i in range(0, 100):  # initialize initial state and random parameters
        for j in range(0, 100):
            state[i][j] = random_vector()
            h[i][j] = (random.random() - 0.5) * 2 * paraW

    try:  # if exist a previous exported file, then use the file data for state[][], else create the file
        file = open(
            "export" + '_' + str(paraG) + '_' + str(paraW) + '_' + str(init_temp) + '_' + str(temp_min) + ".txt", "r+")
    except IOError:
        pass
    else:
        load_state_from_file(file, state)

    while temperature > temp_min:  # annealing
        for circulation in range(0, 100):  # internal circulation for 100 times at same temperature
            for i in range(0, 100):
                for j in range(0, 100):
                    local_update(i, j, temperature)
        print(str(temperature) + " " +
              str(hamiltonian_global()) + " " +
              time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        temperature = 0.95 * temperature

    file = open("export" + '_' + str(paraG) + '_' + str(paraW) + '_' + str(init_temp) + '_' + str(temp_min) + ".txt",
                "w+")
    for i in range(0, 100):  # put the current state into file
        for j in range(0, 100):
            print(state[i][j], file=file)
    file.close()


def load_state_from_file(f, state):
    for i in range(0, 100):
        for j in range(0, 100):
            l = f.readline()
            t = literal_eval(l)  # casting string to tuple
            state[i][j] = t


def plot(state):
    phase = [[0 for i in range(0, 100)] for j in range(0, 100)]
    for i in range(0, 100):
        for j in range(0, 100):
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
    plt.savefig("export" + '_' + str(paraG) + '_' + str(paraW) + '_' + str(init_temp) + '_' + str(temp_min) + ".png")
    plt.show()


def get_args(argv):
    arguments = [0, 0, 0, 0, 0]
    opts, args = getopt.getopt(argv, "hg:w:t:m:f:")
    for opt, arg in opts:
        if opt == '-h':
            print("stimulation.py -g <paraG> -w <paraW> -t <init_temp> -m <temp_min> -f <file>")
            sys.exit()
        if opt == '-g':
            arguments[0] = arg
        if opt == '-w':
            arguments[1] = arg
        if opt == '-t':
            arguments[2] = arg
        if opt == '-m':
            arguments[3] = arg
        if opt == '-f':
            arguments[4] = arg
    return arguments


if __name__ == "__main__":
    h = [[0 for i in range(0, 100)] for j in range(0, 100)]
    state = [[0 for i in range(0, 100)] for j in range(0, 100)]
    args = [0, 0, 0, 0, 0]
    args = get_args(sys.argv[1:])

    paraG = float(args[0])
    paraW = float(args[1])
    init_temp = float(args[2])
    temp_min = float(args[3])
    file_name = args[4]
    if file_name != 0:
        try:
            f = open(file_name,"r")
            load_state_from_file(f,state)
        except IOError:
            print("No such file, or incorrect format")

    calculate(paraG, paraW, init_temp, temp_min)
    plot(state)
    print('\a' * 5)
