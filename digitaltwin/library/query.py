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
import entity
import relation
import nltk
import string
from nltk.util import everygrams
nltk.download('wordnet')

class WrdList:
    def __init__(self, wordlist, wordtype, wordproperty):
        self.wordtype = wordtype
        self.wordlist = wordlist
        self.wordproperty = wordproperty


class QuestionPaser:
    def __init__(self, txt):
        self.txt = txt.lower()
        # TODO create a list of keyword dictionaries, to be match from a natural language question
        with open('nodeList.json') as f:
            self.nodelist = json.load(f)

        ####################################################
        #    Data
        self.wrdsData_index = list(v for v in self.nodelist["Data"]["Data_index"])
        self.wrdListData_index = WrdList(self.wrdsData_index, "Data", "Data_index")
        ######
        self.wrdsTimeStamp = list(v for v in self.nodelist["Data"]["TimeStamp"])
        self.wrdListTimeStamp = WrdList(self.wrdsTimeStamp, "Data", "TimeStamp")
        ######
        self.wrdsuEst_Array = list(v for v in self.nodelist["Data"]["uEst_Array"])
        self.wrdListuEst_Array = WrdList(self.wrdsuEst_Array, "Data", "uEst_Array")
        #####
        self.wrdsuVal_Array = list(v for v in self.nodelist["Data"]["uVal_Array"])
        self.wrdListuVal_Array = WrdList(self.wrdsuVal_Array, "Data", "uVal_Array")
        #####
        self.wrdsyEst_Array = list(v for v in self.nodelist["Data"]["yEst_Array"])
        self.wrdListyEst_Array = WrdList(self.wrdsyEst_Array, "Data", "yEst_Array")
        #####
        self.wrdsyVal_Array = list(v for v in self.nodelist["Data"]["yVal_Array"])
        self.wrdListyVal_Array = WrdList(self.wrdsyVal_Array, "Data", "yVal_Array")
        ####################################################
        #    Model
        self.wrdsModel_name = list(v for v in self.nodelist["Model"]["Model_name"])
        self.wrdListModel_name = WrdList(self.wrdsModel_name, "Model", "Model_name")
        ####################################################
        #    User
        self.wrdsUser_name = list(v for v in self.nodelist["User"]["User_name"])
        self.wrdListUser_name = WrdList(self.wrdsUser_name, "User", "User_name")
        ####################################################
        #    Experiment
        self.wrdsExperiment_name = list(v for v in self.nodelist["Experiment"]["Experiment_name"])
        self.wrdListExperiment_name = WrdList(self.wrdsExperiment_name, "Experiment", "Experiment_name")
        ####################################################
        self.targetWordLists = [self.wrdListData_index, self.wrdListTimeStamp, self.wrdListModel_name, self.wrdListUser_name, self.wrdListExperiment_name]

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
        relationdict = test_relation.Relation.getRelationDict()
        relationEqDict = test_relation.Relation.getEquivalenceDict()
        relationInvDict = test_relation.Relation.getInverseDict()
        entityDict = test_entity.myNode.getNodeDict()

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
            snode = relationdict[r].startnodetype
            enode = relationdict[r].endnodetype
            for i in entities:
                if i[1][0] == snode:
                    sqls.append(
                        f"MATCH (n:{snode})-[r:{r}]->(m:) where n.{i[1][1]} = '{i[0]}' RETURN r")
                if i[1][0] == enode:
                    sqls.append(
                        f"MATCH (n)-[r:{r}]->(m:{enode}) where n.{i[1][1]} = '{i[0]}' RETURN r")

        if not relations:
            for i in entities:
                sqls.append(
                    f"MATCH (n:{[1][0]}) where n.{i[1][1]} = '{i[0]}' RETURN n")

        return sqls, entities, relations, nodeTypes



@bp.route('/home_sub', methods=['GET', 'POST'])
def Query():
    query = request.form['Query']
    #print(query)
    #return "Text extracted successfully"
    
    return render_template("home_2.html", result=query)


