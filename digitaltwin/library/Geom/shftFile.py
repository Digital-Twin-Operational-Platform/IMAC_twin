from ..Service_Layer.Files_Db import FileDb
import csv
import numpy as np
from stl import mesh
import math
from math import atan2

class sftFile:

    def main(self, projectName):
        i = 0   
        db = FileDb()
        csvFile = db.get_files('{proj}\{file}'.format(proj=projectName, file='Position.csv'))

        with open(csvFile, 'r') as loc:
            List = csv.reader(loc, delimiter=',', skipinitialspace=True)
            list_1 = list(filter(lambda x:x, List))

        while i< len(list_1):
            # fileName = list_1[i][0]   # file name for shft. Use shft_before name in yr_mesh
            # Addition of stl saves data in stl format. bcz position file only contains name not file format.
            partname = list_1[i][0] + '.stl'
            fileName =''.join(filter(lambda x: not x.isdigit() , list_1[i][0].replace(".",""))) # file name for non shft
            partFile = db.get_files('{proj}\{file}.stl'.format(proj=projectName, file=fileName))
            base_mesh = mesh.Mesh.from_file(partFile)
            coordinates = list(list_1[i+1][0].replace(")", "").replace("(", "").split(',')) 

            yr_mesh = self.shft_stl(base_mesh, coordinates)
            yield (yr_mesh, partname)

            i = i+2
        
        return 
    
    def shft_stl(self, base_mesh, coordinates):
        a = np.array(coordinates)

        # r1, r2, r3 - rotation aver 1st, 2nd and 3rd axis, and p = translation array
        r1 = np.array_split(a,4)[0].astype(np.float32)    # | 
        r2 = np.array_split(a,4)[1].astype(np.float32)    # |----converting string to decimal as
        r3 = np.array_split(a,4)[2].astype(np.float32)    # |       .rotate takes only numbers and array
        p = np.array_split(a,4)[3].astype(np.float32)     # |

        phi = atan2(r3[1], r3[2])
        theta = atan2(-r3[0], math.sqrt(pow(r3[1],2)+pow(r3[2],2)))
        zeta = atan2(r2[0], r1[0])

        base_mesh.rotate(r1, phi) 
        base_mesh.rotate(r2, theta) 
        base_mesh.rotate(r3, zeta)  

        base_mesh.translate(p)    

        return(base_mesh)