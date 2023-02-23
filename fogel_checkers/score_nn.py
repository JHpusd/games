import sys, random, math, numpy, copy
import numpy.random as nr
sys.path.append('fogel_ttt')
from node import *

class ScoringNeuralNet():
    def __init__(self):
        self.in_layer = []
        self.h1_layer = []
        self.h2_layer = []
        self.out_layer = []
        self.pd_node = None # piece difference node
        self.weights = {}
        self.K = 2
        self.mutat_rate = 0.05
        self.counter = 1
    
    def lin_func(self, x):
        return x
    
    def tanh_func(self, x):
        return math.tanh(x)
    
    def reset_all(self):
        self.in_layer = []
        self.h1_layer = []
        self.h2_layer = []
        self.out_layer = []
        self.pd_node = None # piece difference node
        self.weights = {}
        self.K = 2
        self.counter = 1
    
    def create_layers(self):
        self.reset_all()
        # input layer
        for _ in range(32):
            self.in_layer.append(NetNode(self.counter,self.lin_func))
            self.counter += 1
        self.in_layer.append(NetNode(self.counter,self.lin_func,True))
        self.counter += 1
        # hidden layer 1
        for _ in range(40):
            self.h1_layer.append(NetNode(self.counter,self.tanh_func))
            self.counter += 1
        self.h1_layer.append(NetNode(self.counter,self.tanh_func,True))
        self.counter += 1
        # hidden layer 2
        for _ in range(10):
            self.h2_layer.append(NetNode(self.counter,self.tanh_func))
            self.counter += 1
        self.h2_layer.append(NetNode(self.counter,self.tanh_func,True))
        self.counter += 1
        # output layer
        self.out_layer.append(NetNode(self.counter,self.tanh_func))
        self.counter += 1
        # piece difference node
        self.pd_node = NetNode(self.counter,self.lin_func)
        self.counter += 1
    
    def create_weights(self):
        if len(self.in_layer)==0 or len(self.h1_layer)==0 or len(self.h2_layer)==0 or len(self.out_layer)==0:
            self.create_layers()
        # input layer to hidden layer 1
        for in_node in self.in_layer:
            for h1_node in self.h1_layer:
                if h1_node.bias == True:
                    continue
                rand_weight = random.randint(-200,200) / 1000
                self.weights[f'{in_node.num}{h1_node.num}'] = rand_weight
        # hidden layer 1 to hidden layer 2
        for h1_node in self.h1_layer:
            for h2_node in self.h2_layer:
                if h2_node.bias == True:
                    continue
                rand_weight = random.randint(-200,200) / 1000
                self.weights[f'{h1_node.num}{h2_node.num}'] = rand_weight
        # hidden layer 2 to output layer
        for h2_node in self.h2_layer:
            for out_node in self.out_layer:
                rand_weight = random.randint(-200,200) / 1000
                self.weights[f'{h2_node.num}{out_node.num}'] = rand_weight
        # PD node to output layer
        rand_weight = random.randint(-200,200) / 1000
        self.weights[f'{self.pd_node.num}{self.out_layer[0].num}'] = rand_weight
    
    def get_node(self, node_num):
        if node_num == 87:
            return self.pd_node
        for node in self.in_layer + self.h1_layer + self.h2_layer + self.out_layer:
            if node.num == node_num:
                return node
    
    def nodes_from_weight_str(self, weight_str):
        node_1_num = int(weight_str[:int(len(weight_str)/2)])
        node_2_num = int(weight_str[int(len(weight_str)/2):])
        return [self.get_node(node_1_num), self.get_node(node_2_num)]
    
    def get_weight(self, start, end):
        try:
            return self.weights[f'{start.num}{end.num}']
        except KeyError:
            print('ERROR WITH GETTING WEIGHT')
            return
    
    def reset_nodes(self):
        for node in (self.in_layer+self.h1_layer+self.h2_layer+self.out_layer+[self.pd_node]):
            node.info_from = []
            node.info_to = []
            node.input_val = None
            node.output_val = None
    
    def connect_nodes(self):
        if len(self.weights) == 0:
            self.create_weights()
        self.reset_nodes()
        for key in self.weights:
            nodes = self.nodes_from_weight_str(key)
            nodes[0].info_to.append(nodes[1])
            nodes[1].info_from.append(nodes[0])

    def score_board(self, adjusted_arr):
        # board should be adjusted by player, made len 32
        if len(adjusted_arr) != 32:
            print('input arr must be len 32')
            return
        for i, in_node in enumerate(self.in_layer):
            if in_node.bias:
                in_node.output_val = 1
                continue
            in_node.set_vals(adjusted_arr[i])
        for i, node in enumerate(self.h1_layer + self.h2_layer + self.out_layer):
            if node.bias:
                node.output_val = 1
                continue
            in_val = 0
            for in_node in node.info_from:
                weight = self.get_weight(in_node, node)
                in_val += in_node.output_val * weight
            node.set_vals(in_val)
        return [node.output_val for node in self.out_layer]
    
    def make_copy(self):
        new_net = ScoringNeuralNet()
        new_net.in_layer = copy.deepcopy(self.in_layer)
        new_net.h1_layer = copy.deepcopy(self.h1_layer)
        new_net.h2_layer = copy.deepcopy(self.h2_layer)
        new_net.out_layer = copy.deepcopy(self.out_layer)
        new_net.pd_node = copy.deepcopy(self.pd_node)
        new_net.weights = {key:self.weights[key] for key in self.weights}
        new_net.connect_nodes()
        new_net.counter = int(self.counter)
        return new_net
    
    def replicate(self):
        new_net = self.make_copy()
        
        # mutation rate change
        norm = nr.normal(0,1)
        denom = math.sqrt(2*math.sqrt(len(new_net.weights)))
        coeff = math.e**(norm/denom)
        new_net.mutat_rate = coeff * self.mutat_rate
        
        # weight change
        for key in new_net.weights:
            norm = nr.normal(0,1)
            shift = norm * new_net.mutat_rate
            new_net.weights[key] += shift
        
        # K change
        norm = nr.normal(0,1)
        coeff = math.e**(norm/math.sqrt(2))
        new_net.K = coeff * self.K
        if new_net.K < 1:
            new_net.K = 1
        if new_net.K > 3:
            new_net.K = 3
        
        return new_net

test = ScoringNeuralNet()
print('original nn:')
test.connect_nodes()
print(f'number of weights: {len(test.weights)}')
print(f'mutat rate: {test.mutat_rate}')
print(f'K val: {test.K}')
new_test = test.replicate()
print('replicated nn:')
print(f'number of weights: {len(new_test.weights)}')
print(f'mutat rate: {new_test.mutat_rate}')
print(f'K val: {new_test.K}')