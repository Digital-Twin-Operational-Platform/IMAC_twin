from flask import request, render_template, url_for, redirect, flash, make_response, Blueprint
from ..Geom.Plot import Plot
import numpy as np
from ..Sensor_Locator.Controller import SnsrCont
from .Helper import helperController

bp = Blueprint('Sensor', __name__)

# Uploading and visualisation of new Sensor file
@bp.route('/snsrController', methods=['POST'])
def snsrController():
  #Project name from cookies
  projectName = request.cookies.get('projectName')
  # option to slect exting files in Sensor folder
  hlp = helperController()
  snsrLst = hlp.main(projectName, 'Sensor')

  if request.form['button'] == "New":
    snsrCont = SnsrCont()
    if request.files['ssr_file_name'].filename!='':     
      if request.form['SnsrDatum']:
        datum = request.form['SnsrDatum']
        DatName = str(datum.split('/')[0])
        DatAxs = np.array([])
        DatAxs = np.append(DatAxs, str(datum.split('/')[1]))
        DatAxs = np.append(DatAxs, str(datum.split('/')[2]))
        DatAxs = np.append(DatAxs, str(datum.split('/')[3]))
      else:
        flash('Please Select Datum From CAD!!')
        return redirect(url_for('homeController'))
      
      if request.form.get('Dir'):
        Dir = request.form.get('Dir')
      else:
        flash('Please Select Plane!!')
        return redirect(url_for('homeController'))

      #Array of part files and names
      if request.files['ssr_file_name']:
        filearr = np.array([])
        uploaded_file = request.files['ssr_file_name'] 
        fileName = str(uploaded_file.filename)
        filearr = np.append(filearr, [fileName])
        filearr = np.append(filearr, [uploaded_file])
        filearr = np.split(filearr, len(filearr)/2)
        filearr = np.array(filearr)
        snsrCont.main(projectName, filearr, DatName, DatAxs, Dir)    #SAVING data to db
      else:
        flash('Please Upload File!!')
        return redirect(url_for('homeController'))
      
    else:
      flash('Please Enter a valid Name!!')
      return redirect(url_for('homeController'))
  
  # Visualisation of existing sensor file
  else:
    fileName = request.form.get('snsrFile')
    if fileName == '--select--':
      flash('Please select a sensor file!!')
      return redirect(url_for('homeController'))

  graph = Plot()
  graphJSON=graph.main(projectName, fileName)
  
  return render_template(template_name_or_list='DigiTwin.html', graphJSON=graphJSON, data2 = snsrLst)