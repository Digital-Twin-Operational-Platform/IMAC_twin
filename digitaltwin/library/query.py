'''
'digitaltwin/library/query.py'

:Author:
    Xiaoxue Shen, University of Sheffield

This functions takes the input from the query box on the home page of the app.

'''

from flask import render_template, request
import os

@app.route('/Home', methods=['GET', 'POST'])
def Nominal():
    form={'Query':'What is the material properties of the components?'}
    return render_template('home.html', form=form, date=date)

@app.route('/Home_sub', methods=['GET', 'POST'])
def Query():
    reqest = request.form
    query = request.get('Query')
    print(query)
    return render_template('home.html', form=form, date=date)
