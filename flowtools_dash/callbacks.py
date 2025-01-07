#For modularity and clarity's sake, callbacks are defined here per
#https://stackoverflow.com/questions/62102453/how-to-define-callbacks-in-separate-files-plotly-dash

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, html, dcc, callback, Output, Input, _dash_renderer, State, MATCH, ALL, callback_context, no_update

import figures as figs
import dataloader as dl
import global_dictionary as gd
#Callback template
'''
def get_callbacks(app):
    @app.callback([Output("figure1", "figure")],
                  [Input("child1", "value")])
    def callback1(figure):
        return

    @app.callback([Output("figure2", "figure")],
                  [Input("child2", "value")])
    def callback2(figure):
        return

'''

#Callbacks are funky in Dash. They only use "@" Decorator functions to allow components
#to communicate with other components. 
def get_callbacks(app):
    
    #Update navbar if burger button is pressed. 
    @app.callback(
        Output("appshell", "navbar"),
        Input("burger_button", "opened"), 
        State("appshell", "navbar")
    )
    def navbar_is_open(opened, navbar):
        navbar["collapsed"] = {"mobile": not opened,
                            "desktop": not opened}
        
        return navbar
    
    #Update main graph displayed, along with trace dropdown selection. 
    @app.callback(
        Output("displayed_graph", "figure"),
        Output("trace_dropdown", "data"),
        Output("trace_dropdown", "value"),
        Input("graph_selector","value"),
        running=[(Output("loading_overlay", "visible"), True, False)]
    )
    def main_display(selection):
        graphdict = gd.global_graph_dictionary[selection]
        datalist = []
        traces_metadata = graphdict["traces_metadata_from_name"]
        
        for key in traces_metadata:
            datalist.append(key)
            
        return graphdict["func"]() , datalist, datalist[0]
    
    @app.callback(
        Output({"type": "store", "id": "slider_storage"}, "data"),  #  Stores all sliders together
        Output({"type": "offsetlabel", "id": ALL}, "children"),  #  Updates all labels (including vertical)
        Output({"type": "offsetslider", "id": ALL}, "value"),  #  Ensures sliders retain values
        Input({"type": "offsetslider", "id": ALL}, "value"),  # Listens to all sliders
        Input("graph_selector", "value"),  # Resets sliders when graph changes
        Input("trace_dropdown", "value"),  # Resets sliders when trace changes
        State({"type": "store", "id": "slider_storage"}, "data"),  # Reads stored values
        prevent_initial_call=True  # Ensures callback doesn’t trigger on page load
)
    def update_labels_and_sliders(slider_values, graph_selected, trace_selected, slider_data):
        """
        Updates offset labels dynamically and stores all slider values in one storage space.
        Resets sliders to zero if no stored value exists when switching graphs or traces.
        """

        if not slider_data:
            slider_data = {}

        trace_key = f"{graph_selected}_{trace_selected}"

        #  If trace_selected is None, return dash.no_update as a list for ALL outputs
        if trace_selected is None or graph_selected not in gd.global_graph_dictionary:
            return no_update, [no_update] * 5, [no_update] * 5  # Returns a list for ALL five sliders

        if trace_key not in slider_data:
            slider_data[trace_key] = {}

        # Define default labels for each slider
        slider_labels = {
            "day": "Day Offset",
            "hour": "Hour Offset",
            "minute": "Minute Offset",
            "amplitude": "Amplitude Offset"
        }

        # Get the correct trace units for the vertical offset slider
        trace_units = gd.global_graph_dictionary.get(graph_selected, {}).get("traces_metadata_from_name", {}).get(trace_selected, ["Unknown"])[1]
        slider_labels["vertical"] = f"{trace_units} Offset"  # Uses correct trace unit

        slider_ids = ["day", "hour", "minute", "vertical", "amplitude"]

        # Check what triggered the callback
        triggered_id = callback_context.triggered_id

        stored_slider_values = []
        for i, slider_id in enumerate(slider_ids):
            # If a slider was moved, update only that slider
            if isinstance(triggered_id, dict) and triggered_id.get("type") == "offsetslider":
                if triggered_id["id"] == slider_id:
                    stored_value = slider_values[i]  #  Use live slider value
                else:
                    stored_value = slider_data[trace_key].get(slider_id, 0)  #  Keep stored value
            # If switching graphs/traces, load stored values or reset if none exist
            else:
                stored_value = slider_data[trace_key].get(slider_id, 0)

            stored_slider_values.append(stored_value)

        # Store the new values back in storage
        for i, slider_id in enumerate(slider_ids):
            slider_data[trace_key][slider_id] = stored_slider_values[i]

        # Format labels with updated values
        new_labels = [f"{slider_labels[slider_ids[i]]}: {stored_slider_values[i]}" for i in range(len(slider_ids))]

        return slider_data, new_labels, stored_slider_values
    
