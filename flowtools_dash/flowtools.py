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
#setting up Flask server, which allows us to use advanced caching later on for aa webapp
server = Flask(__name__)
app = Dash(external_stylesheets=dmc.styles.ALL, server=server)
app.config.suppress_callback_exceptions = True 
init_cache(app)

#load/cache default figure while loading webpage
default_figure = figs.stage_x_discharge_wrapper()
default_selection = ["LAG Upstream Height",
                    "LAG Downstream Height",
                    "Frogspot Height",
                    "Oros Height", 
                    "Sepulveda Height",
                    "Sepulveda Discharge"]


#Define webpage structure here. 
appcontents = [
    dmc.AppShell(
        children=[
            #dcc.Store(id="slider_store", storage_type="session", data={}), 
            dcc.Store(id={"type": "store", "id": "slider_storage"}, storage_type="session", data={
                "default_labels": {
                "day": "Day Offset: 0",
                "hour": "Hour Offset: 0",
                "minute": "Minute Offset: 0",
                "vertical": "Vertical Offset: 0",
                "amplitude": "Amplitude Offset: 1"
            }
            }),
            dmc.AppShellHeader(
                dmc.Group(
                    [
                    dmc.Burger(id="burger_button", opened=False),
                    dmc.Title(f"Flowtools", order=1)
                    ],
                    mt=8, p=24
                )
            ),
            dmc.AppShellNavbar(
                id="navbar",
                children=[
                    dmc.SegmentedControl(
                        id="graph_selector",
                        data=[
                            #These "value" labels should match keys in the global graph dictionary,
                            #which can be found in figures.py 
                            {"label": "LAG Stage and Flow", "value":  "stage_x_flow"},
                            {"label":"LA River Temperature", "value": "temperature"}
                            #ADD MORE AS NECESSARY   
                        ],
                        #DEFAULT SELECTION
                        value="stage_x_flow",
                        fullWidth=True,
                        orientation="vertical"
                    )
                    ],
                p="md"
            ),
            dmc.AppShellMain(
                id="main",
                children=[
                    dmc.Center(
                        children=[
                            dmc.Stack(
                                children=[
                                    dmc.LoadingOverlay(
                                    id="loading_overlay",
                                    loaderProps={"type":"dots", "color":"blue","size":"lg"},
                                    overlayProps={"radius":"sm", "blur":2},
                                    zIndex=10,
                                    visible=False
                                    ),
                                    dcc.Graph(id="displayed_graph", figure=default_figure),
                                    
                                dmc.Select(id= "trace_dropdown", data=default_selection, value=default_selection[0], clearable=False, allowDeselect=False),
                                dmc.Grid(children=[
                                    dmc.GridCol(
                                        children=[
                                            html.Label("Days Offset: 0", id={"type":"offsetlabel", "id":"day"}),
                                            dmc.Slider(
                                            #label="Days Offset",
                                            id={"type":"offsetslider", "id":"day"},
                                            value=0,
                                            min=-15,
                                            max=15,
                                            step=1
                                        )
                                        ],
                                        span=4
                                    ),
                                    dmc.GridCol(
                                        children=[
                                            html.Label("Hours Offset: 0", id={"type":"offsetlabel", "id":"hour"}),    
                                            dmc.Slider(
                                                #label="Hours Offset",
                                                id={"type":"offsetslider", "id":"hour"},
                                                value=0,
                                                min=-24,
                                                max=24,
                                                step=1
                                            )
                                        ],
                                        span=4
                                    ),
                                    dmc.GridCol(
                                        children=[
                                            html.Label("Minutes Offset: 0", id={"type":"offsetlabel", "id":"minute"}),
                                            dmc.Slider(
                                            id={"type":"offsetslider", "id":"minute"},
                                            value=0,
                                            min=-60,
                                            max=60,
                                            step=1
                                        )
                                        ],
                                        span=4
                                    ),
                                    dmc.GridCol(
                                        children=[
                                            html.Label("Vertical Offset: 0", id={"type":"offsetlabel", "id":"vertical"}),
                                            dmc.Slider(
                                            #label="Height Offset",
                                            id={"type":"offsetslider", "id":"vertical"},
                                            #default vertical offset values (i.e. for stage height)
                                            #will change in a callback for each trace via dictionary
                                            value=0,
                                            min=-5,
                                            max=5,
                                            step=0.25
                                        )
                                        ],
                                        span=4
                                    ),
                                    dmc.GridCol(
                                        children=[
                                            html.Label("Amplitude: 1", id={"type":"offsetlabel", "id":"amplitude"}),
                                            dmc.Slider(
                                            #label="Amplitude", 
                                            id={"type":"offsetslider", "id":"amplitude"},
                                            value=1,
                                            min=0.1,
                                            max=5,
                                            step=0.1
                                        )
                                        ],
                                        span=4
                                    )
                                ])
                                    
                                    
                                ]
                            )
                            
                        ]
                    )
                ]             
            )
        ],
        header={"height": 100},
        padding="md",
        navbar={
            "width": 300,
            "breakpoint": "sm",
            "collapsed": {"mobile": True},
        },
        id="appshell",
    )
    ]

#Define theming and other aesthetic elements here.
app.layout = dmc.MantineProvider(
     children=appcontents
)

#Use callbacks from Callbacks.py (graph reactions to sliders, selection, etc)
cb.get_callbacks(app)


#debug=True can be used for logging purposes, but should otherwise be False for performance
if __name__ == "__main__":
    app.run(
            debug=True
)
