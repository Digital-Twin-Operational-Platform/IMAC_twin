import glob
from py2neo import Node
import json
import re
import csv
import os.path, time

class myNode(Node):
    @classmethod
    def getsubClasses(cls):
        result = []
        for subclass in cls.__subclasses__():
            result.append(subclass)
        return result

    @classmethod
    def getNodeTypeList(cls):
        result = [a.nodeType for a in cls.getsubClasses()]
        return result

    @classmethod
    def getNodeDict(cls):
        dic = {}
        for a in cls.getsubClasses():
            for b in a.equivalence:
                dic[b] = a.nodeType
        return dic


class Product(myNode):
    identified_by = 'product_name'
    nodeType = "product"
    # The equivalent expression for the node
    equivalence = ["produce", "manufacture", "aftermath"]
    def __init__(self, name_, timeStamp_):
        self.nodeProperties = {}
        self.nodeProperties["product_name"] = name_
        self.nodeProperties["timestamp"] = timeStamp_
        super().__init__(self.nodeType, **self.nodeProperties)


class Component(myNode):
    identified_by = 'component_name'
    nodeType = "component"
    # The equivalent expression for the node
    equivalence = ["produce", "manufacture", "aftermath"]
    def __init__(self, name_):
        self.nodeProperties = {}
        self.nodeProperties["component_name"] = name_
        super().__init__(self.nodeType, **self.nodeProperties)


class Material(myNode):
    identified_by = 'material_name'
    nodeType = "material"
    # The equivalent expression for the node
    equivalence = ["produce", "manufacture", "aftermath"]
    def __init__(self, name_, E_, density_):
        self.nodeProperties = {}
        self.nodeProperties["material_name"] = name_
        self.nodeProperties["youngs_modulus"] = E_
        self.nodeProperties["density"] = density_
        super().__init__(self.nodeType, **self.nodeProperties)


        
        
class Entities():
    list_Product = []
    list_Component = []
    list_Material = []

    @classmethod
    def labeldic(self):
        mydic = {}
        for theNode in myNode.__subclasses__():
            mydic[theNode.nodeType] = theNode.identified_by
        return mydic

    def nodeTodictionary(self, nodes):
        toDic = {}
        for k, v in nodes.items():
            toDic[k] = v
        return toDic
    
    # Transfer a node list to the dictionary(which contains a node as  dictionaries)
    def nodelistTOdictionary(self, nodelist):
        toDic = {}
        for node in nodelist:
            for k, v in node.items():
                if k in toDic and v not in toDic[k]:
                    toDic[k].append(v)
                else:
                    toDic[k] = [v]
        return toDic
    
    def NodeListtoJson(self):  # Export all nodes to json file
        toDic = {}
        toDic["product"] = self.nodelistTOdictionary(
            self.list_Product)
        toDic["component"] = self.nodelistTOdictionary(self.list_Component)
        toDic["material"] = self.nodelistTOdictionary(
            self.list_Material)
        
        with open("nodeList.json", 'w') as f:
            json.dump(toDic, f)
        return toDic

    def add_Product(self, name_, timeStamp_):
        Product_Node = Product(name_, timeStamp_)
        self.list_Product.append(Product_Node)

    def add_Component(self, name_):
        Component_Node = Component(name_)
        self.list_Component.append(Component_Node)

    def add_Material(self, name_, E_, density_):
        Material_Node = Material(name_, E_, density_)
        self.list_Material.append(Material_Node)

    def extractAll_Product_Nodes(self, fileFolder):
        # extract all input information from the file folder
        print("extracting all the nodes information from the files")
        list_ = glob.glob(fileFolder + "*Product*.csv")
        for i in range(0, len(list_)):
            # index_ = re.findall(r'\d+', list_[i])[0]
            # print(index_)
            file_name =  os.path.basename(list_[i])   
            file_name =  re.search('(.*).csv', file_name)
            file_name =  file_name.group(1)
            #result = re.search(fileFolder + '(.*)_dataBenchmark', list_[i])
            #author_ = result.group(1)
            with open(list_[i], newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                timestamp = time.ctime(os.path.getmtime(list_[i]))
                self.add_Product(file_name.lower(), timestamp.lower())
                for row in reader:
                    self.add_Component(row['Component'].lower())
                    count = 0
                    for j in range(0, len(self.list_Material)):
                        if row['Material'] == self.list_Material[j]['material_name']:
                            count += 1
                    if count == 0:
                        self.add_Material(row['Material'].lower(), row['Young Modulus'], row['Density'])
    
        
    def extractAllNodes(self, fileFolder):
        self.extractAll_Product_Nodes(fileFolder)
        self.NodeListtoJson()
        
    def allNodes(self):
        return self.list_Product + self.list_Component + self.list_Material
        
    

# Input_list = glob.glob("/home/shen/Cristallo/dtApp/dtData/knowledgeGraph/*_input.npy")
# num_ = len(Input_list)        

filefolder = "/home/shen/IMAC_twin/digitaltwin/library/Data/"
if __name__ == "__main__":
    print()
    #datafile = pd.ExcelFile("../data/Data.xlsx")
    e = Entities()
    e.extractAllNodes(filefolder)
    #h = e.MaterialNodes()
    #print(len(h))
    #print(h[0]['Material_name'])
    print(e.allNodes())
    # print(Entities.labeldic())
    # e.labeldic()
    

