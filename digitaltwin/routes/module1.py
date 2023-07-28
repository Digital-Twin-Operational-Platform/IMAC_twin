"""
These module python scripts should be designed to:
    1) Add additional URL routes for various computations
    2) Take the Input from the user and convert them to appropriate variables (string to float, etc.)
    3) Call upon the library folder "..library" to perform a function call
    4) Take the output of the library call and render it to the user

For development purposes, all the calculations can be done here, but that will make debugging and unit testing much more difficult.
"""
from ..digitaltwin import bp # the ..digitaltwin tells the directory to look at the parent folder
from flask import render_template

from ..library import query
#from ..library import entity
#from ..library import relation
#from ..library import buildgraph
#from ..library.crossvalidation import graph3
@bp.route("/help")
def help():
    return render_template("help.html")
