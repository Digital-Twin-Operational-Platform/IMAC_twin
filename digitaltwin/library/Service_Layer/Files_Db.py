import os
import sys
from ansys.mapdl.reader import save_as_archive

class FileDb:
    
    # Path to Data\DigiTwins in the library directory of the project
    # For now this is being used as the files database 
    #--Here rootPath gets dir for a folder above it.
    rootPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    fileLoc = os.path.join(rootPath, 'Data\DigiTwins')

    # saves files to a particular project folder
    def save_project(self, projectName, fileName, file):
        path = os.path.join(self.fileLoc, projectName)
        # Creates folder in project name
        # If statement for saving files in loop in same folder
        if not (os.path.isdir(path)):
            os.mkdir(path) 
        path = os.path.join(path, fileName)
        if (fileName.rsplit('.', 1)[1]) == 'msh':
            file.write(path)
        
        elif (fileName.rsplit('.', 1)[1]) == 'cdb':
            save_as_archive (path, file)

        else : file.save(path)
       
        return
    
    #fetches induvidual files
    def get_files(self, fileName):
        file = r"{Loc}\{Name}".format(Loc=self.fileLoc, Name=fileName)
        return (file)
    
    #Checks the existance of folder
    def folder_check(self, folderName):
        path = os.path.join(self.fileLoc, folderName)
        if os.path.isdir(path):
            value = True
        else: value = False
        return (value)
    
    #fetches all files in  the directory
    def list_dir(self, folderName):
        path = os.path.join(self.fileLoc, folderName)
        List = os.listdir(path)        
        # This elemenates folders inside directory
        prtList = list()
        for i in List:
            if (os.path.isfile(os.path.join(path, i))):
                prtList.append(i)
        return (prtList)
    
    #fetches all folders in  the directory
    def list_dir_folder(self, folderName):
        path = os.path.join(self.fileLoc, folderName)
        List = os.listdir(path)        
        # This elemenates files inside directory
        prtList = list()
        for i in List:
            if not (os.path.isfile(os.path.join(path, i))):
                prtList.append(i)
        return (prtList)
    
    def del_file(self, fileName):
        os.remove(r"{Loc}\{Name}".format(Loc=self.fileLoc, Name=fileName))
        return