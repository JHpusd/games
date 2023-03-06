import sys, random, math, numpy, copy
import numpy.random as nr
from score_nn import *

class NeuralNetPlayer():
    def __init__(self, ply, net=None):
        self.number = None
        self.ply = ply
        if net != None:
            self.net = net
        else:
            self.net = ScoringNeuralNet()
        