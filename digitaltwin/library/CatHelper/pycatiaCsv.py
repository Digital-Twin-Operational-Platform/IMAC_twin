import os
import sys
sys.path.insert(0, os.path.abspath('..\\pycatia'))
from pycatia import catia
import csv
from typing import List
from numpy import fromfile

class CATIA:

    def __init__(self) -> None:
        pass

    def pycat (self, fileLoc, fileName):
        
        caa = catia()
        documents = caa.documents
        documents.open(r'{Loc}\{name}.CATProduct'.format(Loc=fileLoc ,name=fileName))
        document = caa.active_document

        product = document.product
        products = product.products

        with open(r'{Loc}\{name}.csv'.format(Loc=fileLoc ,name=fileName),'w') as matrix:
            writer = csv.writer(matrix)
            for product in products:
                writer.writerow([product.name])
                writer.writerow([product.position.get_components()])

        return
    
cat = CATIA()
cat.pycat('Enter File location', 'Enter CATProduct file Name')
