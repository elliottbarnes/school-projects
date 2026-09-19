import numpy as np
import json
import math
import ast
from array import *

class DecisionTree:
    def __init__(self):
        self.nodes = []
        self.root = []
    def createNode(self, split_attr, children):
        node = []
        node.append(split_attr)
        node.append(children)
        self.nodes.append(node)
    
    def toJSON(self):
        return json.dumps(self.root)

decisionTree = DecisionTree()

# this function gets each attribute from a data set and calculates the splitting node
def findSplittingAttribute(data):
    risk = data[0]
    infoD = calculateInfoD(risk)
    infoA_list = []
    for i in range(1, len(data)):
        infoA_list.append(calculateInfoA(data, i))
    class SplittingAttribute:
        def __init__(self):
            self.gain = -1
            self.attr = -1
        def get_attr(self):
            return self.attr
        def set_attr(self, attr):
            self.attr = attr
        def get_gain(self):
            return self.gain
        def set_gain(self, gain):
            self.gain = gain
    splittingAttribute = SplittingAttribute()
    for i in range(len(infoA_list)):
        gain = calculateGain(infoD, infoA_list[i])
        if(i == 0):
            splittingAttribute.set_gain(gain)
            splittingAttribute.set_attr(i)
            continue
        if(gain > splittingAttribute.get_gain()):
            splittingAttribute.set_gain(gain)
            splittingAttribute.set_attr(i)
    return splittingAttribute.attr + 1
    
# this function calculates the expected information needed to classify a tuple 
def calculateInfoD(risk):
    num_high_risk = 0
    info = 0
    total_customers = len(risk)
    #print("total customers:",total_customers)
    #print("risk: ", risk)
    for i in risk:
        if(i == 2):
            num_high_risk += 1
    num_low_risk = total_customers - num_high_risk
    prob_low = num_low_risk / total_customers
    prob_high = num_high_risk / total_customers
    #if((prob_high != 0) and (prob_low != 0)):
    #    info = (prob_low * np.log2(prob_low)) + (prob_high * np.log2(prob_high))
    #    print("Info value", info)
    #    info = -info
    if((prob_high)!= 0):
        info += prob_high*np.log2(prob_high)
    if((prob_low)!=0):
        info += prob_low*np.log2(prob_low)
    info = -info
    return info

# this function loads a training set and calculates the info value of each attribute
def calculateInfoA(data, index):
    vals = set()
    risk = data[0]
    attr = data[index]
    for i in attr:
        vals.add(i)
    infoA = 0
    for val in vals:
        attr_count = 0
        risk_list = []
        for i in range(len(risk)):
            if(attr[i] == val):
                attr_count += 1
                if(risk[i] == 2):
                    risk_list.append(2)
                else:
                    risk_list.append(1)
        infoA += (attr_count / len(attr)) * calculateInfoD(risk_list)
    return infoA

def calculateGain(infoD, infoA):
    return infoD - infoA

def createNode(data, data_desc, split_attr_ind):
    split_attr = data[split_attr_ind]
    risk = data[0]
    branches = set()
    children = {}
    for i in split_attr:
        branches.add(i)
    for branch in branches:
        hi_risk_leaf = True
        lo_risk_leaf = True
        for i in range(len(split_attr)):
            if(split_attr[i] == branch):
                if(risk[i] == 1):
                    hi_risk_leaf = False
                if(risk[i] == 2):
                    lo_risk_leaf = False
        if(hi_risk_leaf == True):
            children[branch] = 2
        elif(lo_risk_leaf == True):
            children[branch] = 1
        else:
            new_data = [[-1]]*(len(data)-1)
            new_data_desc = []
            for i in range(len(data[0])):
                if(split_attr[i] == branch):
                    for j in range(len(data) - 1):
                        if(j < split_attr_ind):
                            if(new_data[j]== [-1]):
                                new_data[j] = [data[j][i]]
                            else:
                                new_data[j].append(data[j][i])
                            new_data_desc.append(data_desc[j])
                        else:
                            if(new_data[j] == [-1]):
                                new_data[j] = [data[j + 1][i]]
                            else:
                                new_data[j].append(data[j+1][i])
                            new_data_desc.append(data_desc[j + 1])
            children[branch] = growTree(new_data, new_data_desc)
    decisionTree.createNode(data_desc[split_attr_ind][0], children)
    return [data_desc[split_attr_ind][0], children]
        
def growTree(data, data_desc):
    split_ind = findSplittingAttribute(data)
    node = createNode(data, data_desc, split_ind)
    return node

# main returns the file where the decision tree is created
def main():

    with open("../data/dataDesc.txt", "r") as f:
        #data_desc = np.array(ast.literal_eval(f.read()))
        data_desc = ast.literal_eval(f.read())
    train = np.loadtxt("../data/train.txt")
    #data_desc = np.loadtxt("../data/dataDesc.txt")
    decisionTree.root = growTree(train, data_desc)
    with open("../data/treeFile.txt", "w") as file:
        json.dump(decisionTree.toJSON(), file)
main()
