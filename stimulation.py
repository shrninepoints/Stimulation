import random
import math
import matplotlib.pyplot as plt
import numpy as np


def random_vector():
    tupSphere = (random.random()*math.pi, random.random()*2*math.pi)  # (theta,phi)
    tupCartesian = (math.sin(tupSphere[0])*math.cos(tupSphere[1]),math.sin(tupSphere[0])*math.sin(tupSphere[1]),math.cos(tupSphere[0]))  # (x,y,z)
    return tupCartesian


def hamiltonian(m, n, vector):  # energy based on environment
    term1 = np.dot(vector, state[(m + 1) % 100][n]) + np.dot(vector, state[(m - 1) % 100][n]) + np.dot(vector, state[m][(n + 1) % 100]) + np.dot(vector, state[m][(n - 1) % 100])
    term2 = paraG * vector[2] * vector[2]
    term3 = h[m][n] * vector[2]
    energy = term1 + term2 + term3
    return energy


def local_update(m,n):  # get a position (m,n), and accept or reject a randomVector result
    newVector = random_vector()
    deltaE = hamiltonian(m,n,state[m][n]) - hamiltonian(m,n,newVector)
    if deltaE < 0:
        state[m][n] = newVector
    else:
        acceptProbability = math.exp(-deltaE/temperature)
        if random.random() < acceptProbability:
            state[m][n] = newVector    # else the state do not change


state = [[0 for i in range(0,100)] for j in range(0,100)]
h = [[0 for i in range(0,100)] for j in range(0,100)]
paraG = 1               # parameters
paraW = 1
temperature = 0.10001
step = 0
for i in range(0,100):   # initialize initial state and random parameters
    for j in range(0,100):
        state[i][j] = random_vector()
        h[i][j] = (random.random() - 0.5) * 2 * paraW

while temperature > 0.1:               # annealing
    for circulation in range(1,1000):  # internal circulation for 1000 times at same temperature
        for i in range(0, 100):
            for j in range(0, 100):
                local_update(i, j)
    step += 1
    temperature = 0.98 * temperature

f = open("export.txt", 'w+')       # export result to doc
for i in range(0,100):
    for j in range(0,100):
        print(state[i][j], file=f)

# TODO: plot the result

