from ..Service_Layer.Files_Db import FileDb
import gmsh as msh
import sys
import pyvista as pv
import numpy as np
import math

class mesh:

    def manual_mesh(self, projectName, meshSize):
        
        db = FileDb()
        msh.initialize()
        msh.model.add("t20")
        srcFolderName = projectName+'\shifted'
        mshFolderName = projectName + '\mesh'

        # Mesh revision
        if (db.folder_check(mshFolderName)):
            #delete old files
            oldFiles = db.list_dir(mshFolderName)
            for file in oldFiles:
                db.del_file(mshFolderName+file)

        # Mesh generation based on input value
        partList = db.list_dir(srcFolderName)

        for part in partList:
            # msh.clear()
            partFile = db.get_files('{proj}\{file}'.format(proj=srcFolderName, file=part))

            # Name to store as cdb
            partName = part.rsplit('.', 1)[0]
            mshName = projectName + meshSize + '.cdb'

            msh.merge(partFile)
            #----------------------------------------Trial1--------------------------
            # n = msh.model.getDimension()
            # s = msh.model.getEntities(n)
            # l = msh.model.geo.addSurfaceLoop([s[i][1] for i in range(len(s))])
            # msh.model.geo.addVolume([l])
            # msh.model.geo.synchronize()
            # msh.option.setNumber("Mesh.SaveAll", 1)
            # # v = msh.model.getBoundary(geom)
            # # msh.model.mesh.setSize(geom, 0.02)
            # msh.model.mesh.generate(3)
            #-----------------------------------------Trial2-Onelab-----------------------------------------------------------
        msh.onelab.set("""[
            {
                "type":"number",
                "name":"Parameters/Angle for surface detection",
                "values":[40],
                "min":20,
                "max":120,
                "step":1
            },
            {
                "type":"number",
                "name":"Parameters/Create surfaces guaranteed to be parametrizable",
                "values":[0],
                "choices":[0, 1]
            },
            {
                "type":"number",
                "name":"Parameters/Apply funny mesh size field?",
                "values":[0],
                "choices":[0, 1]
            }
        ]""")


        angle = msh.onelab.getNumber('Parameters/Angle for surface detection')[0]
        forceParametrizablePatches = msh.onelab.getNumber('Parameters/Create surfaces guaranteed to be parametrizable')[0]

        includeBoundary = True
        curveAngle = 180
        # gmsh.model.mesh.createTopology()
        msh.model.mesh.classifySurfaces(angle * math.pi / 180., includeBoundary, forceParametrizablePatches, curveAngle * math.pi / 180.)
        msh.model.mesh.createGeometry()

        # s = msh.model.getEntities(2)
        # l = msh.model.geo.addSurfaceLoop([e[1] for e in s])
        # msh.model.geo.addVolume([l])

        msh.model.geo.synchronize()

        f = msh.model.mesh.field.add("MathEval")

        if msh.onelab.getNumber('Parameters/Apply funny mesh size field?')[0]:
            msh.model.mesh.field.setString(f, "F", "2*Sin((x+y)/5) + 3")
        else:
            #This method does not provide good control on mesh size. Need to change
            msh.model.mesh.field.setString(f, "F", "{0}".format(meshSize))     # Default value 4
        msh.model.mesh.field.setAsBackgroundMesh(f)

        msh.model.mesh.generate(3)
        # print(mshName)
        #----------------------------------------------------------------------------------------------------------------------------------------

        db.save_project(mshFolderName, 'sample.msh', msh)
        mshFile = db.get_files(mshFolderName + '\sample.msh')
        mesh = pv.read_meshio(mshFile)

        db.save_project(mshFolderName, mshName, mesh)
        db.del_file(mshFolderName + '\sample.msh') 
            # msh.finalize()      
        # msh.finalize()   why isnt this working
        #Visualise
        # if '-nopopup' not in sys.argv:
        #     msh.fltk.run()
       
        return

