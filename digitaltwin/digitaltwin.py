"""
This is the main function that creates the blueprint, imports in the modules, and defines some generic routes such as the home and error pages.
"""
from flask import render_template, request, redirect, url_for, flash, abort, session, jsonify, Blueprint

bp = Blueprint('templateDTOP', __name__) # Creates the name of the app

from .routes import module1

@bp.route('/')
@bp.route('/home')
@bp.route('/index')
def home():
    return render_template('home.html')

@bp.app_errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404