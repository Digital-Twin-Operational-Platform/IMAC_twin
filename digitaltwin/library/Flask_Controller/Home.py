from flask import request, render_template, url_for, redirect, flash, make_response, Blueprint
from ..Geom.Controller import GeomCont
from ..Geom.Plot import Plot
import numpy as np
from ..Service_Layer.Files_Db import FileDb
from .Helper import helperController

bp = Blueprint('Home', __name__)

# Plolty graph to html--------------------
@bp.route('/homeController', methods=['POST', 'GET'])
def homeController():    

    #Save uploaded file to db-----------------------------------------------------------
    Geom = GeomCont()
    db = FileDb()

    if request.method == 'GET':
        projectName = request.cookies.get('projectName')

    elif request.form['button'] == "OldHm":
        #Extracting files from folder and Save
        if request.files['file_name'].filename!='':      #change this after you remove default feedback from html for input
            
            #Check if the project already exists and if the field is filled
            projectName = request.form['Project_Name']

            if (projectName) == '':
                flash ('Please enter project name!!')
                return redirect(url_for('home'))

            elif db.folder_check(projectName):
                flash('The project name already exists. Give a new name')
                return redirect(url_for('home'))
            
            #Array of part files and names
            filearr = np.array([])
            uploaded_file = request.files.getlist('file_name')    
            for f in uploaded_file:
                name = str(f.filename.split('/')[1])
                filearr = np.append(filearr, [name])
                filearr = np.append(filearr, [f])
            filearr = np.split(filearr, len(filearr)/2)
            filearr = np.array(filearr)

            #Checking if position file exits 
            if (len(uploaded_file)) >1:
                if ('Position.csv') in filearr[:,0]:
                    Geom.main(projectName,filearr)                   #SAVING
                else:
                    flash ('Please upload pos')
                    return redirect(url_for('home'))
            #For single part assembly
            elif (len(uploaded_file)) == 1:
                Geom.main(projectName, filearr)                      #SAVING
        
        else:
            flash ('Folder empty! Please re-upload valid data.')
            return redirect(url_for('home'))
        
    else:
        projectName = request.form.get('project')
        if projectName == '--select--':
            flash('Please select a project!!')
            return redirect(url_for('home'))        

    #--------------------------------------------------------------------------------
    # Check if the file is stored in db and if saved display plotly
    # Receiving the plotly graph to render-------------------------------------------
    graph = Plot()
    graphJSON=graph.main(projectName)

    #option to slect exting files in Sensor folder
    hlp = helperController()
    snsrLst = hlp.main(projectName, 'Sensor')

    #Setting project name as jwt - Token to access from different URL's
    response = make_response(render_template(template_name_or_list='DigiTwin.html', graphJSON=graphJSON, data2 = snsrLst))
    response.set_cookie('projectName', projectName)

    return response
