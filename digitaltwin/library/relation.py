# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 10:41:30 2023

@author: me1xs
"""

# from py2neo import Node
import glob
from py2neo import Node
import numpy as np
import re
# from py2neo import Relationship    # added later 

class Relation():
    # Define a relation class which contains index, input, frequency, FRF
    def __init__(self, startNodeType, endNodeType, startNodeID, endNodeID, relationType, bidirection=False, **karg):
        self.startNodeType = startNodeType
        self.endNodeType = endNodeType
        self.startNodeID = startNodeID
        self.endNodeID = endNodeID
        self.property = karg
        self.relationType = relationType
        self.bidirection = bidirection
        # super().__init__(self.startNodeType, self.endNodeType, self.startNodeID, self.endNodeID, self.relationType, self.bidirection)
        
    @classmethod 
    def getsubClasses(cls):   
        result = []
        for subclass in cls.__subclasses__():
            result.append(subclass)
        return result
    
    @classmethod
    def getRelationLabel(cls):
        result = [a.label for a in cls.getsubClasses()]
        return result
    
    @classmethod
    def getRelationDict(cls):
        dic = {}
        for a in cls.getsubClasses():
            dic[a.label] = a
        return dic
    
    @classmethod
    # get the equivalence(synonym) dictionary for relations
    def getEquivalenceDict(cls):
        dic = {}
        for a in cls.getsubClasses():
            for b in a.equivalence:
                if b in dic:
                    dic[b].append(a.label)
                else:
                    dic[b] = [a.label]
        return dic

    @classmethod
    def getInverseDict(cls):  # get the inverse(antonym) dictionary for relations
        dic = {}
        for a in cls.getsubClasses():
            for b in a.inverse:
                if b in dic:
                    dic[b].append(a.label)
                else:
                    dic[b] = [a.label]
        return dic

    def __str__(self):
        if self.bidirection == False:
            return(f"Relation(({self.startNodeType}:{self.startNodeID})-({self.relationType}:{self.property})->({self.endNodeType}:{self.endNodeID})")
        else:
            return(f"Relation(({self.startNodeType}:{self.startNodeID})-({self.relationType}:{self.property})-({self.endNodeType}:{self.endNodeID})")

    def __repr__(self):
        if self.bidirection == False:
            return(f"Relation(({self.startNodeType}:{self.startNodeID})-({self.relationType}:{self.property})->({self.endNodeType}:{self.endNodeID})")
        else:
            return(f"Relation(({self.startNodeType}:{self.startNodeID})-({self.relationType}:{self.property})-({self.endNodeType}:{self.endNodeID})")



class User2Data(Relation):
    label = "User_created_Data"
    startNodeType = "User"
    endNodeType = "Data"
    inverse = ['data created by user']
    equivalence = ['generated', "input", "produced"]
    def __init__(self, username, Data_index):
        super().__init__(self.startNodeType, self.endNodeType, username, Data_index, self.label)


class Model2Data(Relation):
    label = "learning_from"
    startNodeType = "Model"
    endNodeType = "Data"
    inverse = ['Train the Model']
    equivalence = ['parameters', "system input"]
    def __init__(self, Model_name, Data_name):
        super().__init__(self.startNodeType, self.endNodeType,Model_name, Data_name, self.label, bidirection=True)

class Model2User(Relation):
    label = "Input_output"
    startNodeType = "Model"
    endNodeType = "User"
    inverse = ['Data to Model']
    equivalence = ['parameters', "system input"]
    def __init__(self, Model_name, User_name):
        super().__init__(self.startNodeType, self.endNodeType,Model_name, User_name, self.label, bidirection=True)

class Model2Experiment(Relation):
    label = "Input_output"
    startNodeType = "Model"
    endNodeType = "Experiment"
    inverse = ['Data to Model']
    equivalence = ['parameters', "system input"]
    def __init__(self, Model_name, Experiment_name):
        super().__init__(self.startNodeType, self.endNodeType,Model_name, Experiment_name, self.label, bidirection=True)


##########################################
class Relations:
    rel_User2Data = []
    rel_Model2Data = []
    rel_Model2User = []
    rel_Model2Experiment = []
    

    def add_User2Data(self, User_name, Data_index):
        r = User2Data(User_name, Data_index)
        self.rel_User2Data.append(r)

    def add_Model2Data(self, Model_name, Data_name):
        r = Model2Data(Model_name, Data_name)
        self.rel_Model2Data.append(r)

    def add_Model2User(self, Model_name, User_name):
        r = Model2User(Model_name, User_name)
        self.rel_Model2User.append(r)

    def add_Model2Experiment(self, Model_name, Experiment_name):
        r = Model2Experiment(Model_name, Experiment_name)
        self.rel_Model2Experiment.append(r)

        
    def extractAllRelation(self, fileFolder):
        print("extracting all the relations")
        ############################################
        ############################################
        self.add_Model2Data("Average", "Data")
        self.add_Model2User("Average", "User")
        self.add_Model2Experiment("Average", "Experiment")
        list_ = glob.glob(fileFolder + "*dataBenchmark*.csv")
        for i in range(0, len(list_)):
            index_ = re.findall(r'\d+', list_[i])[0]
            result = re.search(fileFolder + '(.*)_dataBenchmark', list_[i])
            author_ = result.group(1)
            self.add_User2Data(author_, index_)
            print(i)
            
    
    def allRelations(self):
        return self.rel_User2Data + self.rel_Model2Data + self.rel_Model2User + self.rel_Model2Experiment
        
filefolder = "/home/shen/TEC_twin/knowledgeGraph/Data/"
if __name__ == "__main__":
    #e = Relations()
    #e.extractAllRelation(filefolder)
    #print(e.allRelations())
    print("")
        

    
        
        
    
    
    
    
        
    
