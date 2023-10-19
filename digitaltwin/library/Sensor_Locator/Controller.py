from ..Service_Layer.Files_Db import FileDb
from .Sensor import Sensor
import csv

class SnsrCont:
    
    def main(self, projectName, filearr, DatName, DatAxs, Dir):

        db = FileDb()
        ssrName = projectName + '\\' + 'Sensor' + '\\'
        Snsr = Sensor()
        #store base file       
        db.save_project(ssrName, filearr[0][0], filearr[0][1])
        csv_file = db.get_files(ssrName + '\\' + filearr[0][0])

        with open(csv_file, 'a', newline='') as file:
            write = csv.writer(file)
            write.writerow('')
            write.writerow([DatName])
            write.writerow(DatAxs)
            write.writerow(Dir)
            file.close()
        file = Snsr.main(projectName, filearr[0][0])

        return
    

