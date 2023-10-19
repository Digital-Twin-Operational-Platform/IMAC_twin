from ..Service_Layer.Files_Db import FileDb
import csv
import numpy as np
from decimal import Decimal
from io import StringIO
from .Maximus import fnd_z
import pandas as pd

class Sensor:

    def main(self, projectName, sensorName):
            
        db = FileDb()
        file = projectName + '\Sensor\\' + sensorName 
        file = db.get_files(file)

        # Part Name, Reference point and 'Plane of measurement'
        df = pd.read_csv(file, names=list(range(3)))
        Dat = df.tail(3)
        Dat = Dat.to_numpy()
        PartName = Dat[0][0]
        Ref = np.array([])
        Ref = np.append(Ref, Dat[1][0]) #X
        Ref = np.append(Ref, Dat[1][1]) #Y
        Ref = np.append(Ref, Dat[1][2]) #Z
        Dir = Dat[2][0] + Dat[2][1]
        DirfrCsv = np.array([Dat[2][0], Dat[2][1]])
        
        # Sensor location measurements in the 'Plane of measurement'
        data = pd.read_csv(file, skipfooter=3, engine='python')
        snsrdt = data.to_numpy()
        val = np.array([])
        
        if Dir == 'xy':
            coord1 = np.asfarray(snsrdt[:, 0]) + float(Ref[0])
            coord2 = np.asfarray(snsrdt[:, 1]) + float(Ref[1])
            snsrdt = np.column_stack((coord1, coord2))
            fndz = fnd_z()      #Automation to find elavation of point on surface
            ElevPts = np.array(list(fndz.main(projectName, PartName, snsrdt, 1, 2)))  # elev = 2 means third axis. x,y,z ===> 0,1,2,, Dir = 1 means positive surface, 0 means negative surface
            val = np.column_stack((snsrdt, ElevPts))
        
        if Dir == 'yz':
            coord1 = np.asfarray(snsrdt[:, 0]) + float(Ref[1])
            coord2 = np.asfarray(snsrdt[:, 1]) + float(Ref[2])
            snsrdt = np.column_stack((coord1, coord2))
            fndz = fnd_z()      #Automation to find elavation of point on surface
            ElevPts = np.array(list(fndz.main(projectName, PartName, snsrdt, 1, 0)))  # elev = 2 means third axis. x,y,z ===> 0,1,2,, Dir = 1 means positive surface, 0 means negative surface
            val = np.stack((ElevPts, coord1, coord2), axis=1)
        
        if Dir == 'zx':
            coord1 = np.asfarray(snsrdt[:, 0]) + float(Ref[0])
            coord2 = np.asfarray(snsrdt[:, 1]) + float(Ref[2])
            snsrdt = np.column_stack((coord1, coord2))
            fndz = fnd_z()      #Automation to find elavation of point on surface
            ElevPts = np.array(list(fndz.main(projectName, PartName, snsrdt, 1, 1)))  # elev = 2 means third axis. x,y,z ===> 0,1,2,, Dir = 1 means positive surface, 0 means negative surface
            val = np.stack((coord2, ElevPts, coord1), axis=1)

        
        #Create temp csv file
        with open(file, 'w', newline='') as ssav:
            wr = csv.writer(ssav, delimiter=',')
            wr.writerows(val)
            wr.writerow([PartName])
            wr.writerow(Ref)
            wr.writerow(DirfrCsv)

        return ()
    
    def getVal(self, projectName, sensorName):
        
        db = FileDb()

        #If user selects group of sensors
        if sensorName == 'All':
            folderName = projectName + '\Sensor'
            files = db.list_dir(folderName)
            x = np.array([])
            y = np.array([])
            z = np.array([])
            for file in files:
                name = folderName + '\\' + file
                file = db.get_files(name)
                df = pd.read_csv(file, skipfooter=3, engine='python')
                data = df.to_numpy()
                x = np.concatenate((x,data[:, 0]))
                y = np.concatenate((y, data[:, 1]))
                z = np.concatenate((z, data[:, 2])) 
        # if user select specific sensor
        else:
            file = projectName+ '\Sensor\\' + sensorName
            file = db.get_files(file)
            df = pd.read_csv(file, skipfooter=3, engine='python')
            data = df.to_numpy()
            x = data[:, 0]
            y = data[:, 1]
            z = data[:, 2] 

        return(x,y,z)
    
# sns = Sensor()
# sns.main('s')