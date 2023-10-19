from ..Service_Layer.Files_Db import FileDb
import numpy as np

class helperController:
    # Fuction returns files in a given folder like Sensor and Mesh to display in select tag html
    def main(self, projectName, folderName):

        #option to slect exting files in Sensor folder
        db = FileDb()
        snsrLst = np.array([])
        if db.folder_check('{0}\{1}'.format(projectName, folderName)):
            files = db.list_dir('{0}\{1}'.format(projectName, folderName))
            snsrLst = np.array(['--select--', 'All'])
            for file in files:
                snsrLst= np.append(snsrLst, file)

        return (snsrLst)

