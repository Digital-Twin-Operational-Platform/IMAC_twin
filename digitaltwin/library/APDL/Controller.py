from .gMesh import mesh
from .Ansys_FEA import ansys
from ..Service_Layer.Files_Db import FileDb

class fea:

    def main(self, projectName, meshSize, fileName = ''):

        db = FileDb()
        msh = mesh()
        slv = ansys()

        if fileName == '':
            msh.manual_mesh(projectName, meshSize)
            mshName = projectName + meshSize + '.cdb'
            mshFile = db.get_files(projectName+ '\Mesh' + mshName)
            slv.main(mshFile)

        return
    
# cont = fea()
# cont.main()