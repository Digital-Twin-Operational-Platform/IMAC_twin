'''
'digitaltwin/library/query.py'

:Author:
    Xiaoxue Shen, University of Sheffield

This functions takes the input from the query box on the home page of the app.

'''

from flask import render_template, request
import os
from ..digitaltwin import bp

@bp.route('/Home', methods=['GET', 'POST'])
def Nominal():
    form={'Query':'What is the material  properties of the components?'}
    return render_template('home.html', form=form, date=date)

@bp.route('/home_sub', methods=['GET', 'POST'])
def Query():
    query = request.form['Query']
    print(query)
    #return "Text extracted successfully"
    return render_template("home_2.html")

'''
<!--<td><input type="text" id="Query" name="Query" step=any value="{{form['Query']}}"></td> -->
'''
