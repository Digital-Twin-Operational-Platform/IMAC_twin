# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 14:09:23 2023

@author: me1xs
"""

from py2neo import Graph, Node, NodeMatcher
import entity as et
import relation as rel
import time
import glob
import csv
import os.path
import re

class BuildGraph:
    # a BuildGraph class takes a list of nodes and edges
    def __init__(self, nodes, edges):
        self.g = Graph("http://localhost:7474", auth=("neo4j", "123456"))   #  7474 or 7687
        self.nodes = nodes
        self.edges = edges
        
    def createNodes(self, *nodes):
        # A function to create nodes in the Neo4j graph database from the list of nodes
        for node in nodes:
            self.g.create(node)
            
    def deleteAll(self):
        self.g.delete_all()
        
    def createRelations(self, *relations):
        # create a relationship on the Neo4j graph
        labeldict = et.Entities.labeldic()
        # print(labeldict)
        # tx = self.g.begin()
        # i = 0
        for r in relations:
            # print(r.__repr__())
            # tx.create(r)
            #print(r.property.items())
            # self.g.create(r)
            if r.bidirection == False:
                query = f"match (p:{r.startNodeType}) " +\
                    f"match (q:{r.endNodeType}) " +\
                    f"where p.{labeldict[r.startNodeType]} = '{r.startNodeID}' and q.{labeldict[r.endNodeType]} = '{r.endNodeID}' " +\
                    f"merge(p)-[r:{r.relationType}] -> (q) "
            else:
                query = f"match (p: {r.startNodeType}) " +\
                    f"match(q: {r.endNodeType}) " +\
                    f"where p.{labeldict[r.startNodeType]} = '{r.startNodeID}' and q.{labeldict[r.endNodeType]} = '{r.endNodeID}' " +\
                    f"merge(p)-[r:{r.relationType}]->(q)"
            for k, v in r.property.items():
                addQuery = f"set r.{k}='{v}' \n"
                query = query + " " + addQuery
            self.g.run(query)
            print(query)
            # print(r.bidirection)
    
    def initialize(self):
        #   initialize the neo4j knowledge graph using the data assigned to the graph attributes
        #   clear graph
        self.deleteAll()
        #   create all nodes in the Neo4j database
        self.createNodes(*self.nodes.allNodes())
        # print("Finished 4")
        #   create all edges in the Neo4j database 
        self.createRelations(*self.edges.allRelations())
        # print(*self.edges.allRelations())
        print("")

    def GraphUpdate(self):
        self.createNodes(*self.nodes.allNodes())
        self.createRelations(*self.edges.allRelations())
        
    def countAllnodes(self):
        print("Nodes: ", len(self.g.nodes))
        print("Edges: ", len(self.g.relationships))
    

filefolder = "/home/shen/IMAC_twin/digitaltwin/library/Data/"
if __name__ == "__main__":
    #   create a Entities object which stores different kinds of nodes
    n = et.Entities()
    e = rel.Relations()
    #   extract all nodes and relations 
    n.extractAllNodes(filefolder)
    e.extractAllRelation(filefolder)
    #   create a BuildGraph object
    g = BuildGraph(n, e)
    # print("Finished 5")
    g.initialize()
    print("Finished")
    g.countAllnodes()
    """
    ##############
    count = 0
    list_ = glob.glob(filefolder + "/dataBenchmark*.csv")
    Number_files = len(list_)    # Check the number of files at T=0
    
    while 1:
        time.sleep(10)
        count += 10
        list_ = glob.glob(filefolder + "/dataBenchmark*.csv")    # Check again the number of files
        print("System is running: ", count, " seconds")
        if len(list_) > Number_files:
            Number_files += 1                                    # Update the number by adding 1
            print("Updating the knowledge graph")
            list_ = glob.glob(filefolder + "/dataBenchmark*.csv")
            index_ = re.findall(r'\d+', list_[-1])[0]
            with open(list_[-1], newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                uEst_, uVal_, yEst_, yVal_ = [], [], [], []
                for row in reader:
                    uEst_.append(float(row['uEst']))
                    uVal_.append(float(row['uVal']))
                    yEst_.append(float(row['yEst']))
                    yVal_.append(float(row['yVal']))

            ####################################
            a = et.TimeStamp(index_, time.ctime(os.path.getmtime(list_[-1])))    # Create Node a
            b = et.uEst(index_, uEst_)                                           # Create Node b
            r = rel.timeStamp2uEst(index_, index_)                               # Create relation r
            g.createNodes(a)
            g.createNodes(b)
            g.createRelations(r)
            g.countAllnodes()
            ###################################
            #et.add_TimeStamp(index_, time.ctime(os.path.getmtime(list_[-1])))
            #et.add_uEst(index_, uEst_)
            #timeStamp2uEst = rel.timeStamp_to_uEst
            #g.createNodes(a)
            #g.countAllnodes()
            #g.g.merge(rel.timeStamp2uEst(a, b))
    """
"""
    while 1:
        g.run("MATCH (p:)")
    
            
        
query = f"match (p:{r.startNodeType}) " +\
                    f"match (q:{r.endNodeType}) " +\
                    f"where p.{labeldict[r.startNodeType]} = '{r.startNodeID}' and q.{labeldict[r.endNodeType]} = '{r.endNodeID}' " +\
                    f"merge(p)-[r:{r.relationType}] -> (q) "    
        
        
query = f"match (p:{r.}) " +\
                    f"match (q:{r.endNodeType}) " +\
                    f"where p.{labeldict[r.startNodeType]} = '{r.startNodeID}' and q.{labeldict[r.endNodeType]} = '{r.endNodeID}' " +\
                    f"merge(p)-[r:{r.relationType}] -> (q) "        
"""        
        
        
        
    
                       
