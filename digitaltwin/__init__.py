"""
This __init__.py can create global functions that can be called by any modules. Things to investigate include bootstrap js/html for global 
front-end functions, class defintions, and various "app" related functions/variables.
"""
from flask_bootstrap import Bootstrap5
from flask import Flask

def create_app(test_config = None):
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    bootstrap = Bootstrap5(app)

    from . import digitaltwin
    app.register_blueprint(digitaltwin.bp)

    from .library.Flask_Controller import Home, Mesh, Sensor
    app.register_blueprint(Home.bp)
    app.register_blueprint(Mesh.bp)
    app.register_blueprint(Sensor.bp)

    return app

