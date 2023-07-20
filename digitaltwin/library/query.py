'''
'digitaltwin/library/query.py'

:Author:
    Xiaoxue Shen, University of Sheffield

This functions takes the input from the query box on the home page of the app.

'''

from flask import render_template, request
import os
from ..digitaltwin import bp
import json
#import entity
#import relation
from ..library import entity
from ..library import relation
import nltk
import string
from py2neo import Graph, Node, NodeMatcher
from nltk.util import everygrams
# nltk.download('wordnet')
# nltk.download('punkt')
# nltk.download('omw-1.4')

class WrdList:
    def __init__(self, wordlist, wordtype, wordproperty):
        self.wordtype = wordtype
        self.wordlist = wordlist
        self.wordproperty = wordproperty


class QuestionPaser:
    def __init__(self, txt):
        self.txt = txt.lower()
        # TODO create a list of keyword dictionaries, to be match from a natural language question
        with open('/home/shen/IMAC_twin/digitaltwin/library/nodeList.json') as f:
            nodelist = json.load(f)
            # print(nodelist)
            self.nodelist = {k.lower(): { m.lower(): [o.lower() for o in n] for m, n in v.items()} for k, v in nodelist.items()}
            #print(self.nodelist)

        ####################################################
        #    Data
        self.wrdsProduct_name = list(v for v in self.nodelist["product"]["product_name"])
        self.wrdListProduct_name = WrdList(self.wrdsProduct_name, "product", "product_name")
        ######
        self.wrdsProduct_TimeStamp = list(v for v in self.nodelist["product"]["timestamp"])
        self.wrdListProduct_TimeStamp = WrdList(self.wrdsProduct_TimeStamp, "product", "timestamp")
        ######
        self.wrdsComponent_name = list(v for v in self.nodelist["component"]["component_name"])
        self.wrdListComponent_name = WrdList(self.wrdsComponent_name, "component", "component_name")
        #####
        self.wrdsMaterial_name = list(v for v in self.nodelist["material"]["material_name"])
        self.wrdListMaterial_name = WrdList(self.wrdsMaterial_name, "material", "material_name")
        #####
        self.wrdsMaterial_YoungModulus = list(v for v in self.nodelist["material"]["youngs_modulus"])
        self.wrdListMaterial_YoungModulus = WrdList(self.wrdsMaterial_YoungModulus, "material", "youngs_modulus")
        #####
        self.wrdsMaterial_Density = list(v for v in self.nodelist["material"]["density"])
        self.wrdListMaterial_Density = WrdList(self.wrdsMaterial_Density, "material", "density")
        ####################################################
        ####################################################
        self.targetWordLists = [self.wrdListProduct_name, self.wrdListProduct_TimeStamp, self.wrdListComponent_name, self.wrdListMaterial_name, self.wrdListMaterial_YoungModulus, self.wrdListMaterial_Density, self.wrdListMaterial_Density]

    def wrddict(self):  # build a dictionary key as {name:[*wordtype]}
        wd_dict = {}
        for i in self.targetWordLists:
            for j in i.wordlist:
                if j.lower() not in wd_dict:
                    wd_dict[j.lower()] = [(i.wordtype, i.wordproperty)]
                else:
                    wd_dict[j.lower()].append((i.wordtype, i.wordproperty))
        return wd_dict

    def wrdkeys(self):
        return self.nodelist.keys()

    def checkwords(self):
        result = []
        for word in self.nGram(3):
            a = self.wrddict().get(word, False)
            if a != False:
                result.append(a)
        return result

    def nGram(self, n):  # To deal with phrases,split all words into the list with the maximum of n words
        a = list(everygrams(self.parseQuestion(), max_len=3))
        b = [" ".join(word) for word in a]
        return b

    def parseQuestion(self):  # Split the question sentense into words
        lem = nltk.WordNetLemmatizer()
        tokenized_text = nltk.word_tokenize(self.txt.lower())
        parsed = [
            lem.lemmatize(word) for word in tokenized_text if word[0] not in string.punctuation]
        return parsed

    def toSqls(self):
        sqls = []
        relations = []
        entities = []
        nodeTypes = []
        parsedQuestion = self.nGram(3)
        wrdDict = self.wrddict()
        relationdict = relation.Relation.getRelationDict()
        relationEqDict = relation.Relation.getEquivalenceDict()
        relationInvDict = relation.Relation.getInverseDict()
        entityDict = entity.myNode.getNodeDict()
        
        for word in parsedQuestion:
            if word in wrdDict:
                for v in wrdDict[word]:
                    entities.append((word, v))
                nodeTypes.append(wrdDict[word][0][0])
            if word in relationEqDict:
                for v in relationEqDict[word]:
                    relations.append(v)
            if word in relationInvDict:
                for v in relationInvDict[word]:
                    relations.append(v)
            if word in entityDict:
                nodeTypes.append(entityDict[word])

        for r in relations:
            snode = relationdict[r].startNodeType
            enode = relationdict[r].endNodeType
            snode = snode.lower()
            enode = enode.lower()
            print(snode, enode)
            for i in entities:
                if i[1][0] == snode:
                    sqls.append(
                        f"MATCH (n:{snode})-[r:{r}]->(m: {enode}) where n.{i[1][1]} = '{i[0]}' RETURN m")
                if i[1][0] == enode:
                    sqls.append(
                        f"MATCH (n)-[r:{r}]->(m:{enode}) where n.{i[1][1]} = '{i[0]}' RETURN r")

        if not relations:
            for i in entities:
                sqls.append(
                    f"MATCH (n:{[1][0]}) where n.{i[1][1]} = '{i[0]}' RETURN n")
        
        return sqls, entities, relations, nodeTypes

"""    
q = QuestionPaser("What is the material name of Nut_4mm.22")
g = Graph("http://localhost:7474", auth=("neo4j", "123456"))

results = g.run("MATCH (n:component)-[r:is_made_of]->(m: material) where n.component_name = 'nut_4mm.22' RETURN m").data()
print(results)
"""

@bp.route('/home_sub', methods=['GET', 'POST'])
def Query():
    query = request.form['Query']
    print(query)
    g = Graph("http://localhost:7474", auth=("neo4j", "123456"))
    q =  QuestionPaser(str(query))
    print(q.toSqls()[0][0])
    results = g.run(q.toSqls()[0][0]).data()
    print(results)
    return render_template("home_2.html", result=results)


