#std lib
import copy, gc
from datetime import date, datetime, timedelta

#third party
import numpy as np
import pandas as pd
import requests 

import dash_mantine_components as dmc
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc, callback, Output, Input, _dash_renderer, State
from flask import Flask
from plotly.subplots import make_subplots


#local
from cache import cache, init_cache
import dataloader as dl 
import figures as figs
import callbacks as cb


#Reference docs
#https://dash.plotly.com/dash-core-components/slider
#https://plotly.com/python/line-and-scatter/

#useful tools we could use
#https://dash-bootstrap-components.opensource.faculty.ai/
#https://www.dash-leaflet.com/
#https://www.dash-mantine-components.com/
#https://community.plotly.com/t/community-components-index/60098


#SPECIAL CONSIDERATION
#Plotly Resampler is a very promising tool, but its development isn't completed yet. It is also 
#difficult to install, requiring even more dependencies than Dash does. 
#https://predict-idlab.github.io/plotly-resampler/v0.9.0/getting_started/#register_plotly_resampler

#Dash Extensions 
#Has a lot of useful serverside features, like caching. Exactly what we needed. 
#https://www.dash-extensions.com/

#Dash Iconify
#Icons usable with Dash Mantine Components 
#https://icon-sets.iconify.design/

#nice-to-have variables 
palette = px.colors.qualitative
colors = palette.Plotly

#setting up Dash using Dash Mantine Components, which uses an older version of React
_dash_renderer._set_react_version("18.2.0")
#setting up Flask server, which allows us to use advanced caching later on for a webapp
server = Flask(__name__)
app = Dash(external_stylesheets=dmc.styles.ALL, server=server)
init_cache(app)

#Define webpage structure here. 
appcontents = []

#Define theming and other aesthetic elements here.
app.layout = dmc.MantineProvider(
     children=appcontents
)

#Use callbacks from Callbacks.py (graph reactions to sliders, selection, etc)
#cb.get_callbacks(app)

#debug=True can be used for logging purposes, but should otherwise be False for performance
if __name__ == "__main__":
    app.run(
            debug=True
            )
