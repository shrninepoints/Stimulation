"""
State stores a current state of the lattice, in the form of ((x, y, z), (theta, phi))

"""


import math
import numpy as np
import matplotlib.pyplot as plt
from ast import literal_eval
import sys


class State:

    def __init__(self, file = '', paraG = 0, paraW = 0):
        self.state = [[self.random_vector() for i in range(0, 100)] for j in range(0, 100)]
        # which stores the current state
        self.h = [[self.random_vector() for i in range(0, 100)] for j in range(0, 100)]
        # h is the random field
        self.paraG = paraG
        self.paraW = paraW
        self.file: str = file  # file name, not file itself
        if file != '':
            try:
                f = open(file, "r")
                self.load_state_from_file(f)

            except IOError:
                print("No such file, or incorrect format")
                sys.exit(1)

    def print(self):
        f = open(self.file, "r+")
        for i in range(0, 100):  # put the current state into file
            for j in range(0, 100):
                print(state[i][j], file=f)
        print(self.paraG, file=f)
        print(self.paraW, file=f)

    def plot(self):  # TODO: check
        phase = [[0 for i in range(0, 100)] for j in range(0, 100)]
        for i in range(0, 100):
            for j in range(0, 100):
                phase[i][j] = self.state[i][j][1][0] * 2 - 1  # revert cartesian to sphere coordinate
        for j in range(100):
            x = [i for i in range(100)]
            y = [j for i in range(100)]
            plt.scatter(x, y, c=phase[j], marker="s", s=4)
        plt.colorbar()
        plt.savefig("export" + '_' + str(self.paraG) + '_' + str(self.paraW) + ".png")
        plt.show()

    def load_state_from_file(self, f):
        for i in range(0, 100):
            for j in range(0, 100):
                l = f.readline()
                t = literal_eval(l)  # casting string to tuple
                self.state[i][j] = t

    @staticmethod
    def random_vector() -> tuple:
        tupSphere = (np.random.rand(), np.random.rand() * 2)  # (theta,phi)
        tupCartesian = (math.sin(tupSphere[0] * math.pi) * math.cos(tupSphere[1] * math.pi),
                        math.sin(tupSphere[0] * math.pi) * math.sin(tupSphere[1] * math.pi),
                        math.cos(tupSphere[0] * math.pi))  # (x,y,z)
        return (tupCartesian, tupSphere)

    @staticmethod
    def random_vector_normal(previousVector: tuple) -> tuple:
        # an improvise of random_vector(), aiming for high accept probability. previousVector is a tuple of (theta, phi)
        tupSphere = ((np.random.normal(0, 0.1) + previousVector[0]) % 1,
                     (np.random.normal(0, 0.2) + previousVector[1]) % 2)
        tupCartesian = (math.sin(tupSphere[0] * math.pi) * math.cos(tupSphere[1] * math.pi),
                        math.sin(tupSphere[0] * math.pi) * math.sin(tupSphere[1] * math.pi),
                        math.cos(tupSphere[0] * math.pi))  # (x,y,z)
        return (tupCartesian, tupSphere)

    def hamiltonian_local(self, m, n, vector):  # energy based on environment
        term1: float = np.dot(vector, self.state[(m + 1) % 100][n][0]) + \
                       np.dot(vector, self.state[(m - 1) % 100][n][0]) + \
                       np.dot(vector, self.state[m][(n - 1) % 100][0]) + \
                       np.dot(vector, self.state[m][(n + 1) % 100][0])
        term2: float = self.paraG * vector[2] * vector[2]
        term3: float = self.h[m][n] * vector[2]
        energy: float = - term1 / 2 - term2 + term3
        return energy

    def hamiltonian_global(self):
        energy: float = 0
        for i in range(0, 100):
            for j in range(0, 100):
                energy += self.hamiltonian_local(i, j, self.state[i][j][0])
        return energy


