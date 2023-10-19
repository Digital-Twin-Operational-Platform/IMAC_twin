# Using Default values for material property. 
# Should add pick and select mesh and material features for induvidual parts in frontend 

from flask import request, render_template, url_for, redirect, flash, make_response, Blueprint
import numpy as np
from ..APDL.Controller import fea
from .Helper import helperController

bp = Blueprint('Mesh', __name__)

# Uploading and visualisation of new Sensor file
@bp.route('/mshController', methods=['POST', 'GET'])
def mshController():
    #Project name from cookies
    projectName = request.cookies.get('projectName')
    
    mshSize = request.form['MSize']
    msh = fea()
    msh.main(projectName, mshSize)


    response = make_response(redirect(url_for('homeController')))

    return response