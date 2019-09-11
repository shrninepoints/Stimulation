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
import plot
import sys, getopt


def random_vector():
    tupSphere = (random.random(), random.random() * 2)  # (theta,phi)
    tupCartesian = (math.sin(tupSphere[0] * math.pi)*math.cos(tupSphere[1] * math.pi),math.sin(tupSphere[0] * math.pi)*math.sin(tupSphere[1] * math.pi),math.cos(tupSphere[0] * math.pi))  # (x,y,z)
    return (tupCartesian, tupSphere)


def random_vector_normal(previousVector):  # an improvise of random_vector(), aiming for high accept probability
    tupSphere = ((np.random.normal(0, 0.1) + previousVector[0]) % 1, (np.random.normal(0, 0.2) + previousVector[1]) % 2)
    tupCartesian = (math.sin(tupSphere[0] * math.pi)*math.cos(tupSphere[1] * math.pi),math.sin(tupSphere[0] * math.pi)*math.sin(tupSphere[1] * math.pi),math.cos(tupSphere[0] * math.pi))  # (x,y,z)
    return (tupCartesian, tupSphere)


def hamiltonian(m, n, vector):  # energy based on environment
    term1 = np.dot(vector, state[(m + 1) % 100][n][0]) + np.dot(vector, state[(m - 1) % 100][n][0]) + np.dot(vector, state[m][(n + 1) % 100][0]) + np.dot(vector, state[m][(n - 1) % 100][0])
    term2 = paraG * vector[2] * vector[2]
    term3 = h[m][n] * vector[2]
    energy = term1 + term2 + term3
    return energy


def local_update(m,n, temperature):  # get a position (m,n), and accept or reject a randomVector result
    newVector = random_vector_normal(state[m][n][0])
    deltaE = hamiltonian(m,n,state[m][n][0]) - hamiltonian(m,n,newVector[0])
    if deltaE < 0:
        state[m][n] = newVector
    else:
        acceptProbability = math.exp(-deltaE/temperature)
        if random.random() < acceptProbability:
            state[m][n] = newVector    # else the state do not change


def calculate(G, W, init_temp, temp_min):
    paraG = G
    paraW = W
    temperature = init_temp
    for i in range(0,100):   # initialize initial state and random parameters
        for j in range(0,100):
            state[i][j] = random_vector()
            h[i][j] = (random.random() - 0.5) * 2 * paraW

    try:        # if exist a previous exported file, then use the file data for state[][], else create the file
        file = open("export" + ' ' + str(paraG) + ' ' + str(paraW) + ".txt", "r+")
    except IOError:
        pass
    else:
        plot.load_state_from_file(file, state)

    while temperature > temp_min:               # annealing
        for circulation in range(1,1000):  # internal circulation for 100 times at same temperature
            for i in range(0, 100):
                for j in range(0, 100):
                    local_update(i, j, temperature)
        temperature = 0.98 * temperature

    file = open("export" + ' ' + str(paraG) + ' ' + str(paraW) + ".txt", "w+")
    for i in range(0,100):              # put the current state into file
        for j in range(0,100):
            print(state[i][j], file=file)
    file.close()

def cal_args(argv):
    opts, args = getopt.getopt(argv, "hg:w:t:m:", ["ifile=", "ofile="])
    for opt, arg in opts:
        if opt == '-h':
            print("stimulation.py -g <paraG> -w <paraW> -t <init_temp> -m <temp_min>")
            sys.exit()
        if opt == '-g':
            paraG = arg
        if opt == '-w':
            paraW = arg
        if opt == '-t':
            init_temp = arg
        if opt == '-m':
            temp_min = arg
    calculate(paraG, paraW, init_temp,temp_min)


if __name__ == "__main__":
    paraG = 0
    paraW = 0
    h = [[0 for i in range(0, 100)] for j in range(0, 100)]
    state = [[0 for i in range(0,100)] for j in range(0,100)]

    cal_args(sys.argv[1:])
    # calculate()
    plot.plot(state)
