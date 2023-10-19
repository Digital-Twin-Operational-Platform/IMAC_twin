from stl import mesh
import numpy as np
from ..Service_Layer.Files_Db import FileDb

class fnd_z :

    def main(self, projectName, partName, snsrData, dir, elv): 
    # elev = 2 means third axis. x,y,z ===> 0,1,2,, Dir = 1 means positive surface, 0 means negative surface

        db = FileDb()
        file = projectName + '\shifted\\' + partName 
        file = db.get_files(file)

        your_mesh = mesh.Mesh.from_file(file)

        # column for binary search
        bnDir = 0     #Along x axis
        if elv == 0:
            bnDir = 1  #Along y axis

        #self, tar, dir, fnd, projectName, sensorName
        # vertices1 = np.array(your_mesh.v0)
        # vertices1 = vertices1[vertices1[:,elv].argsort()]
        # vertices1 = (np.array_split(vertices1, 2))[dir]    # this is to split points belonging to upper and lower surface. Needs better logic
        vertices1 = np.unique(your_mesh.v0, axis=0)
        med = np.unique(vertices1[:, elv], axis=0)
        medval = np.median(med)
        vertices1 = vertices1[vertices1[:, elv]>medval]
        vertices1 = vertices1[vertices1[:,bnDir].argsort()]
              
        # vertices2 = np.array(your_mesh.v1)
        # vertices2 = vertices2[vertices2[:,elv].argsort()]
        vertices2 = np.unique(your_mesh.v1, axis=0)
        med = np.unique(vertices2[:, elv], axis=0)
        medval = np.median(med)
        vertices2 = vertices2[vertices2[:, elv]>medval]
        # vertices2 = (np.array_split(vertices2, 2))[dir]
        vertices2 = vertices2[vertices2[:,bnDir].argsort()]

        # vertices3 = np.array(your_mesh.v0)
        # vertices3 = vertices3[vertices3[:,elv].argsort()]
        # vertices3 = (np.array_split(vertices3, 2))[dir]
        vertices3 = np.unique(your_mesh.v2, axis=0)
        med = np.unique(vertices3[:, elv], axis=0)
        medval = np.median(med)
        vertices3 = vertices3[vertices3[:, elv]>medval]      # Add a if condition for direction
        vertices3 = vertices3[vertices3[:,bnDir].argsort()]

        for tar in snsrData:
            ver1 = self.binary_search(vertices1, tar, bnDir)
            ver2 = self.binary_search(vertices1, tar, bnDir)
            ver3 = self.binary_search(vertices1, tar, bnDir)
            rslt = (ver1[0][elv] + ver2[0][elv] + ver3[0][elv])/3   #Add logic for not taking average rather getting beter height from vertices
            # rslt = ver1[0][elv]
            yield rslt

        return()

    def binary_search(self, vertices, target, dir):

        x = target[dir]
        i = 0
        
        while len(vertices[:, dir]) > 1:

            j = len(vertices)
            if (j % 2) == 0:
                j = int(j/2)
            else:
                j = int((j-1)/2)
            # vertices = (np.array_split(vertices, 2))[0]
            # print((vertices[0]))

            if (x > vertices[j][dir]):
                vertices = (np.array_split(vertices, 2))[1]
            #     print(vertices)
            #     vertices = np.split(vertices, len(vertices)/3)
            
            elif (x < vertices[j][dir]):
                vertices = (np.array_split(vertices, 2))[0]
            #     print(vertices)
            #     vertices = np.split(vertices, len(vertices)/3)
            # print(vertices)

        return(vertices)

