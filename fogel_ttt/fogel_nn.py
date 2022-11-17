import random, math, numpy, copy
from node import *

class FogelEvolvingNet():
    def __init__(self):
        self.num_H = random.randint(1,10)
        self.in_layer = []
        self.h_layer = []
        self.out_layer = []
        self.weights = {}
        self.counter = 1
    
    def create_layers(self):
        # input layer
        func = lambda x: x
        for _ in range(9):
            self.in_layer.append(NetNode(self.counter, func))
            self.counter += 1
        self.in_layer.append(NetNode(self.counter, func, True))
        self.counter += 1
        # hidden layer
        func = lambda x: 1/(1+(math.e)**-x)
        for _ in range(self.num_H):
            self.h_layer.append(NetNode(self.counter, func))
            self.counter += 1
        self.h_layer.append(NetNode(self.counter, func, True))
        self.counter += 1
        # output layer
        for _ in range(9):
            self.out_layer.append(NetNode(self.counter, func))
            self.counter += 1
    
    def create_weights(self):
        if len(self.in_layer)==0 or len(self.h_layer)==0 or len(self.out_layer)==0:
            print('CREATE LAYERS BEFORE CREATING WEIGHTS')
            return
        for in_node in self.in_layer:
            for h_node in self.h_layer:
                if h_node.bias == True:
                    continue
                rand_weight = random.randint(-500,500) / 1000
                self.weights[f'{in_node.num}{h_node.num}'] = rand_weight
        for h_node in self.h_layer:
            for out_node in self.out_layer:
                rand_weight = random.randint(-500,500) / 1000
                self.weights[f'{h_node.num}{out_node.num}'] = rand_weight
    
    def get_node(self, node_num):
        for node in self.in_layer + self.h_layer + self.out_layer:
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
        for node in (self.in_layer + self.h_layer + self.out_layer):
            node.info_from = []
            node.info_to = []
            node.input_val = None
            node.output_val = None
    
    def connect_nodes(self):
        if len(self.weights) == 0:
            print('CREATE WEIGHTS BEFORE CONNECTING NODES')
            return
        self.reset_nodes()
        for key in self.weights:
            nodes = self.nodes_from_weight_str(key)
            nodes[0].info_to.append(nodes[1])
            nodes[1].info_from.append(nodes[0])
    
    def input_array(self, input_arr):
        if len(input_arr) != 9:
            print('input array must be len 9')
            return
        for i,node in enumerate(self.in_layer):
            if node.bias:
                node.output_val = 1
                continue
            node.set_vals(input_arr[i])
        for i,node in enumerate(self.h_layer + self.out_layer):
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
        new_net = FogelEvolvingNet()
        new_net.in_layer = copy.deepcopy(self.in_layer)
        new_net.h_layer = copy.deepcopy(self.h_layer)
        new_net.out_layer = copy.deepcopy(self.out_layer)
        new_net.weights = {key:self.weights[key] for key in self.weights}
        new_net.connect_nodes()
        new_net.counter = int(self.counter)
        return new_net
    
    def add_h_node(self):
        if len(self.h_layer) == 11:
            return
        func = lambda x: 1/(1+(math.e)**-x)
        new_node = NetNode(self.counter, func)
        self.h_layer.append(new_node)
        self.counter += 1

        for in_node in self.in_layer:
            self.weights[f'{in_node.num}{new_node.num}'] = 0
        for out_node in self.out_layer:
            self.weights[f'{new_node.num}{out_node.num}'] = 0
        self.connect_nodes()
    
    def del_h_node(self):
        if len(self.h_layer) == 2:
            return
        # delete from num_H, h_layer, weights
        rand_node = random.choice([node for node in self.h_layer if not node.bias])
        del_weights = []
        for key in self.weights:
            if rand_node in self.nodes_from_weight_str(key):
                del_weights.append(key)
        for key in del_weights:
            del self.weights[key]
        self.num_H -= 1
        self.h_layer.remove(rand_node)
        # delete from other nodes
        for in_node in self.in_layer:
            in_node.info_to.remove(rand_node)
        for out_node in self.out_layer:
            out_node.info_from.remove(rand_node)
    
    def replicate(self): # all replicated nets are initialized
        new_net = self.make_copy()
        # weight incrementing
        for key in new_net.weights:
            increm = numpy.random.normal(0,0.05)
            new_net.weights[key] += increm
        # hidden layer add/delete
        mod_bool = random.choice([True, False])
        if mod_bool:
            add_bool = random.choice([True, False])
            if add_bool:
                new_net.add_h_node()
            else: # delete case
                new_net.del_h_node()

        return new_net
    
    def initialize(self):
        if len(self.in_layer) != 0:
            return
        self.create_layers()
        self.create_weights()
        self.connect_nodes()
                
'''
net = FogelEvolvingNet()
net.initialize()

print([n.num for n in net.out_layer])
print([n.num for n in net.h_layer])
print([n.num for n in net.in_layer])
print(net.input_array([0,0,0,0,0,0,0,0,0]))
print(len(net.weights))
new_net = net.replicate()
print([n.num for n in new_net.out_layer])
print([n.num for n in new_net.h_layer])
print([n.num for n in new_net.in_layer])
print(new_net.input_array([0,0,0,0,0,0,0,0,0]))
print(len(new_net.weights))
#print(net.weights)
'''