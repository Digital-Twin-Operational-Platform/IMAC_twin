from ..Service_Layer.Files_Db import FileDb
from .shftFile import sftFile

class GeomCont:
    
    def main(self, projectName, filearr):

        db = FileDb()
        #store base file
        for f in filearr : 
            db.save_project(projectName, f[0], f[1])

        shft = sftFile()
        #store shifted file
        for file, name in shft.main(projectName):
            folder = projectName + '\shifted'
            db.save_project(folder, name, file)

        #deleting unwanted object to free up space
        del file, name, filearr

        return
    
