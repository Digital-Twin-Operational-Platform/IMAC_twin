'''
This function compares the experimental FRFs of each structure with the simulated FRFs of their respective numerical models.
'''
from flask import render_template

import plotly
from plotly.subplots import make_subplots
import numpy as np
import json

from .extract_data import tSW,tSO,tSH,tBR,youtSW,youtSO,youtSH,youtBR
from .extract_data import tNumSW,tNumSWmiddle,tNumSO,tNumSH,tNumBR,tNumSHmiddle,youtNumSW,youtNumSO,youtNumSH,youtNumBR


fig3 = make_subplots(rows=1, cols=1)

# Fig3.a
fig3.add_scatter(x=tSW,y=youtSW[:,0], name='Experiment', mode = 'lines', row=1, col=1)
fig3.add_scatter(x=tNumSW,y=youtNumSW[:,0], name='FEM', mode = 'markers', marker=dict(size= 1.5), row=1, col=1)
# Update xaxis properties
fig3.update_xaxes(title_text="Freq (Hz)", titlefont=dict(size=15), row=1, col=1)
# Update yaxis properties
fig3.update_yaxes(title_text="dB", titlefont=dict(size=15),row=1,col=1)

fig3.update_layout(height=250, width=250, margin=dict(l=1, r=1, t=1, b=1))
#fig3.update_layout(title_text="<b>FRF<b>")
fig3.update_layout(showlegend=True, legend=dict(x=1, y=1, xanchor='right', yanchor='top', bgcolor='rgba(0, 0, 0, 0)'), font=dict(size=11))
#fig3.update_layout(title={'y':0.99,'x':0.6,'xanchor': 'center'})
graph3 = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
