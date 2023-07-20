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
import os
import csv
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



class Product2Component(Relation):
    label = "contains"
    startNodeType = "product"
    endNodeType = "component"
    inverse = ['belongs_to']
    equivalence = ['includes', "has", "consists"]
    def __init__(self, Product_name, Component_name):
        super().__init__(self.startNodeType, self.endNodeType, Product_name, Component_name, self.label)


class Component2Material(Relation):
    label = "is_made_of"
    startNodeType = "component"
    endNodeType = "material"
    inverse = ['makes']
    equivalence = ['contains', "has", "material name"]
    def __init__(self, Component_name, Material_name):
        super().__init__(self.startNodeType, self.endNodeType,Component_name, Material_name, self.label, bidirection=True)



##########################################
class Relations:
    rel_Product2Component = []
    rel_Component2Material = []    

    def add_Product2Component(self, Product_name, Component_name):
        r = Product2Component(Product_name, Component_name)
        self.rel_Product2Component.append(r)

    def add_Component2Material(self, Component_name, Material_name):
        r = Component2Material(Component_name, Material_name)
        self.rel_Component2Material.append(r)
        
    def extractAllRelation(self, fileFolder):
        print("extracting all the relations")
        ############################################
        list_ = glob.glob(fileFolder + "*Product*.csv")
        for i in range(0, len(list_)):
            file_name =  os.path.basename(list_[i])   
            file_name =  re.search('(.*).csv', file_name)
            file_name =  file_name.group(1)
            with open(list_[i], newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    self.add_Product2Component(file_name.lower(), row['Component'].lower())
                    self.add_Component2Material(row['Component'].lower(), row['Material'].lower())
                    
    
    def allRelations(self):
        return self.rel_Product2Component + self.rel_Component2Material
        
filefolder = "/home/shen/IMAC_twin/digitaltwin/library/Data/"
if __name__ == "__main__":
    #e = Relations()
    #e.extractAllRelation(filefolder)
    #rint(e.allRelations())
    print("")
        
    
        
        
    
    
    
    
        
    
