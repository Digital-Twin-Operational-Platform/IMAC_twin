from ..Service_Layer.Files_Db import FileDb
from ansys.mapdl.core import launch_mapdl 
import numpy as np

class ansys:

    def main(self, mshFile):
        mapdl = launch_mapdl(loglevel="ERROR")
        # folder = r'C:\Users\me1pd\Desktop\Projects\Plotly_FEA\Files_Db\Trial\mesh'
        # mshFiles = db.list_dir(folder)
        # mapdl.clear()
        mapdl.cdread('db', mshFile)
        mapdl.prep7()
        
        mapdl.shpp("SUMM")
        # mapdl.eshape(0, 0)
        mapdl.eplot(show_node_numbering=True)
        
        mapdl.sectype(1, "shell")
        # # mapdl.secread(r'C:\Users\me1pd\Desktop\Projects\Plotly_FEA\Files_Db\Mimick\mesh\RCC.2')
        mapdl.secdata(0.1)
        # # mapdl.keyopt('GCN',3,2)
        # # mapdl.keyopt('GCN', 2, 0)
        # # mapdl.gcgen('UPDATE') 
        # # mapdl.gcgen('NEW')         # Default or auto contact generation

        mapdl.emodif("ALL", "SECNUM", 1)

        mapdl.units("SI")  # not necessary, but helpful for book keeping
        mapdl.mp("EX", 2, 71e9)  # Elastic moduli in Pa (kg/(m*s**2))
        mapdl.mp("DENS", 2, 2710)  # Density in kg/m3
        mapdl.mp("NUXY", 2, 0.3)  # Poissons Ratio
        mapdl.emodif("ALL", "MAT", 2)


        mapdl.d(933, "ALL", 0)
        mapdl.d(935, "ALL", 0)
        mapdl.d(938, "ALL", 0)
        mapdl.d(934, "ALL", 0)
        mapdl.d(906, "ALL", 0)
        mapdl.d(905, "ALL", 0)
        mapdl.d(907, "ALL", 0)
        mapdl.d(908, "ALL", 0)
        mapdl.d(870, "ALL", 0)
        mapdl.d(871, "ALL", 0)
        mapdl.d(879, "ALL", 0)
        mapdl.d(868, "ALL", 0)
        mapdl.d(939, "ALL", 0)
        mapdl.d(941, "ALL", 0)
        mapdl.d(942, "ALL", 0)
        mapdl.d(948, "ALL", 0)
        
        mapdl.modal_analysis(nmode=10, freqb=100) # set number of modes and frequency
        # print(4)
        mapdl.slashsolu()
        mapdl.solve()
        result = mapdl.result
        # print(5)
    
        cpos = result.animate_nodal_solution(3) # select the mode number to animate
        result.animate_nodal_solution(0) 
        result.animate_nodal_solution(6)
        result.animate_nodal_solution(9)
        return


