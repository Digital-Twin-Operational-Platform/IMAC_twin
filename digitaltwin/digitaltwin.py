"""
This is the main function that creates the blueprint, imports in the modules, and defines some generic routes such as the home and error pages.
"""
from flask import render_template, request, redirect, url_for, flash, abort, session, jsonify, Blueprint
from .library.Service_Layer.Files_Db import FileDb
import numpy as np
import os

bp = Blueprint('IMAC_DTOP', __name__) # Creates the name of the app

from .routes import module1

# from .library.crossvalidation import graph3

@bp.route('/')
@bp.route('/home')
@bp.route('/index')
@bp.route('/home_sub')
def home():
    # Method to allow reload of same page. Sample
    if request.method == 'POST':
        post_data = dict(request.form)
        if os.path.exists(post_data['directory'][0]):
            return redirect(url_for('home'))
        else:
            flash('Directory does not exist !')
            return redirect(url_for('home'))
    #----------------------------------------------

    #option to select exting Projects
    db = FileDb()
    files = db.list_dir_folder('')
    option1 = np.array(['--select--'])
    for file in files:
        option1= np.append(option1, file)

    return render_template('Index.html')

@bp.app_errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404
