import plotly
import plotly.graph_objects as go
import numpy as np
from stl import mesh
from math import atan2
import json
from ..Service_Layer.Files_Db import FileDb
from ..Sensor_Locator.Sensor import Sensor

class Plot:

    def main(self, projectName, sensorName = False):
        
        I = np.array([])
        J = np.array([])
        K = np.array([])
        fileName = projectName + '\shifted'
        i = 0   
        db = FileDb()
        prtList = db.list_dir(fileName)
        
        for part in prtList:
            partname = part
            prtfile = db.get_files('{proj}\{file}'.format(proj=fileName, file=partname))
            yr_mesh = mesh.Mesh.from_file(prtfile)

            p, q, r = yr_mesh.vectors.shape
            unq_vertcs = np.unique(yr_mesh.vectors.reshape(p*q, r), axis = 0)
            I, J, K = self.ijk(yr_mesh, unq_vertcs)
            X, Y, Z = unq_vertcs.T
            
            if i == 0:
                fig = go.Figure((go.Mesh3d(x=X, y=Y, z=Z, i=I, j=J, k=K, hovertemplate='{0}'.format(partname)+'<extra></extra>', name=partname)))
                # Alternate - hovertemplate = partname + '<extra></extra>'
            else:
                fig.add_trace((go.Mesh3d(x=X, y=Y, z=Z, i=I, j=J, k=K, hovertemplate='{0}'.format(partname)+'<extra></extra>', name=partname)))

            i = i+1
        
        #Sensor Markers
        if sensorName is not False:
            ssr = Sensor()
            x, y, z = ssr.getVal(projectName, sensorName)
            fig.add_trace(go.Scatter3d(x=z, y=y, z=x, mode='markers', marker=dict(color='black', size=6)))

        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', width=800, height=800)
        figure = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return (figure)

    #Finds I J K values
    def ijk (self, yr_mesh, unq_vertcs):

        I = np.array([])
        J = np.array([])
        K = np.array([])
            
        # value for I
        for k in yr_mesh.v0:
            # pos = np.where(np.all((k==unq_vertcs), axis=1))[0][0]
            pos = self.arrInArr(k, unq_vertcs)
            I = np.append(I, pos)

        # value for I
        for k in yr_mesh.v1:
            # pos = np.where(np.all((k==unq_vertcs), axis=1))[0][0]
            pos = self.arrInArr(k, unq_vertcs)
            J = np.append(J, pos)
    
        # value for I
        for k in yr_mesh.v2:
            # pos = np.where(np.all((k==unq_vertcs), axis=1))[0][0]
            pos = self.arrInArr(k, unq_vertcs)
            K = np.append(K, pos)
        
        return(I, J, K)

    #Finds loc of arra in multidimensional array

    #--------------Method1 arrInArr (Most time consuming)----------------------------
    # def arrInArr(self, fndKIn, Arr):
    #     i = 0
    #     for k in Arr:
    #         if (fndKIn[0] == k[0]) :
    #             if (fndKIn[1] == k[1]) :
    #                 if (fndKIn[2] == k[2]):
    #                     return i
    #         i += 1
        # return 

    #--------------- Method2 arrInArr------------------------------------------------
    # def arrInArr(self, fndKIn, Arr):
    #     pos = np.where(np.all((fndKIn==Arr), axis=1))[0][0]
    #     return (pos)

    #----Method2 arrInArr (Fastest. Works for Hwk and 3-storey structure. Needs tuning against more models)-------
    def arrInArr(self, fndKIn, Arr, X=0, Y=1, Z=2, i=0):
        # print(fndKIn)
        while len(Arr[:, X]) > 1:
            
            j = int(len(Arr[:, X])/2) #For odd array gives central elemnt; For even gives first elemnet of second array

            # if the arra exists in the central element
            if (fndKIn[X]==Arr[j][X]):
                if (fndKIn[Y]==Arr[j][Y]) & (fndKIn[Z]==Arr[j][Z]):
                    i = i + j 
                    return(i)
                else:
                    # Collect new array of equal X elemnts
                    counter = 0
                    jPlus = j+1
                    jMin = j-1

                    # Based on the initial while loop we assume there should be a elemnt before j at this stage.
                    while (Arr[j][X] == Arr[jMin][X]):
                        if counter != 0:
                            jMin = jMin-1
                        counter = counter + 1
                        if (counter < len(Arr[0:(j) , :3])):
                            continue
                        else: break
                   
                    counter = 0

                    # Check if the array ends at j
                    if len(Arr[j:len(Arr[:, X]), :3]) > 1:
                        while (Arr[j][X] == Arr[jPlus][X]):
                            jPlus = jPlus + 1
                            counter = counter + 1
                            if (counter < len(Arr[(j+1):len(Arr[:, X]) , :3])):
                                continue
                            else: break  
                        Arr = Arr[jMin:jPlus, :3]   
                    else: Arr = Arr[jMin:j, :3]      
                    
                    i = i + jMin
    
                    for elm in Arr:
                        if (fndKIn[Y]==elm[Y]) & (fndKIn[Z]==elm[Z]):
                            return i 
                        else: i = i+1
            
            elif (fndKIn[X] > Arr[j][X]):
                Arr = Arr[(j+1):len(Arr[:, X]), :3]
                i = i + j + 1
            
            elif (fndKIn[X] < Arr[j][X]):
                Arr = Arr[0:j, :3]

        return(i)
