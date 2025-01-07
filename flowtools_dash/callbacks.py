#For modularity and clarity's sake, callbacks are defined here per
#https://stackoverflow.com/questions/62102453/how-to-define-callbacks-in-separate-files-plotly-dash

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, html, dcc, callback, Output, Input, ctx, State, MATCH, ALL, callback_context, no_update, Patch
from datetime import timedelta, datetime
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
        Output("displayed_graph", "figure", allow_duplicate=True),
        Output("trace_dropdown", "data"),
        Output("trace_dropdown", "value"),
        Output("original_graph_store", "data"),
        Input("graph_selector","value"),
        running=[(Output("loading_overlay", "visible"), True, False)]
    )
    def main_display(selection):
        graphdict = gd.global_graph_dictionary[selection]
        #datalist = []
        #traces_metadata = graphdict["traces_metadata_from_name"]
        
        #for key in traces_metadata:
         #   datalist.append(key)
        datalist = list(graphdict["traces_metadata_from_name"].keys())
        newgraph = graphdict["func"]()
        return newgraph , datalist, datalist[0], newgraph
    
    @app.callback(
    Output({"type": "store", "id": "slider_storage"}, "data"),  #  Stores all sliders together
    Output({"type": "offsetlabel", "id": ALL}, "children"),  # Updates all labels (including vertical)
    Output({"type": "offsetslider", "id": ALL}, "value"),  #  Ensures sliders retain values
    Input({"type": "offsetslider", "id": ALL}, "value"),  #  Listens to all sliders
    Input("graph_selector", "value"),  #  Resets sliders when graph changes
    Input("trace_dropdown", "value"),  #  Resets sliders when trace changes
    State({"type": "store", "id": "slider_storage"}, "data"),  #  Reads stored values
    prevent_initial_call=True
)
    def update_labels_and_sliders(slider_values, graph_selected, trace_selected, slider_data):
        """
        Updates offset labels dynamically and stores all slider values in one storage space.
        Ensures sliders default correctly when loading and retain values when moved.
        """

        if not slider_data:
            slider_data = {}

        trace_key = f"{graph_selected}_{trace_selected}"

        if trace_selected is None or graph_selected not in gd.global_graph_dictionary:
            return no_update, [no_update] * 5, [no_update] * 5  #  Prevents errors

        if trace_key not in slider_data:
            slider_data[trace_key] = {}

        #  Define correct default values
        slider_defaults = {
            "day": 0,
            "hour": 0,
            "minute": 0,
            "vertical": 0,
            "amplitude": 1  #  Ensures amplitude defaults to 1
        }

        slider_labels = {
            "day": "Day Offset",
            "hour": "Hour Offset",
            "minute": "Minute Offset",
            "amplitude": "Amplitude Offset"
        }

        trace_units = gd.global_graph_dictionary[graph_selected]["traces_metadata_from_name"][trace_selected][1]
        slider_labels["vertical"] = f"{trace_units} Offset"

        slider_ids = list(slider_defaults.keys())

        #  Identify what triggered the callback
        triggered_id = callback_context.triggered_id

        stored_slider_values = []
        if triggered_id == "graph_selector":
            stored_slider_values = list(slider_defaults.values())
        else:
            for i, slider_id in enumerate(slider_ids):
                #  If a slider was moved, prioritize its value
                if isinstance(triggered_id, dict) and triggered_id.get("type") == "offsetslider":
                    if triggered_id["id"] == slider_id:
                        stored_value = slider_values[i]  #  Use live slider value
                    else:
                        stored_value = slider_data[trace_key].get(slider_id, slider_defaults[slider_id])  #  Keep stored value
                else:
                    stored_value = slider_data[trace_key].get(slider_id, slider_defaults[slider_id])  #  Load stored value

                stored_slider_values.append(stored_value)

        slider_data[trace_key] = dict(zip(slider_ids, stored_slider_values))
        
        

        new_labels = [f"{slider_labels[slider_ids[i]]}: {stored_slider_values[i]}" for i in range(len(slider_ids))]

        return slider_data, new_labels, stored_slider_values
    
    @app.callback(
        Output("displayed_graph", "figure"),
        Input({"type": "offsetslider", "id": ALL}, "value"),
        State("trace_dropdown", "value"),
        State("graph_selector", "value"),
        State("original_graph_store", "data"),
        prevent_initial_call=True
    )
    def update_trace(offsets, trace_selected, graph_selected, original_graph):
        """Updates the selected trace with vertical offset & amplitude scaling."""
        
        # Ensure valid data
        if not original_graph or "data" not in original_graph:
            return no_update
        
        # Get list of slider IDs (to match them with the offsets)
        slider_ids = [slider["id"]["id"] for slider in ctx.inputs_list[0]]

        # Extract individual slider values
        vertical_offset = offsets[slider_ids.index("vertical")]
        amplitude = offsets[slider_ids.index("amplitude")]
        day = offsets[slider_ids.index("day")]
        hour = offsets[slider_ids.index("hour")]
        minute = offsets[slider_ids.index("minute")]
        

        # Identify which slider was changed
        triggered_id = ctx.triggered_id
        
        if not isinstance(triggered_id, dict) or triggered_id.get("type") != "offsetslider":
            return no_update

        # Create a patched figure
        patched_figure = Patch()

        # Identify the trace index from the graph dictionary
        graphdict = gd.global_graph_dictionary[graph_selected]
        trace_idx = graphdict["traces_metadata_from_name"][trace_selected][0]

        # Compute mean value of the original y-data
        mean_value = np.mean(original_graph["data"][trace_idx]["y"])

        comparableid = triggered_id.get("id")
        match comparableid:
            case "vertical" | "amplitude":
                patched_figure["data"][trace_idx]["y"] = [
                    (y - mean_value) * amplitude + mean_value + vertical_offset for y in original_graph["data"][trace_idx]["y"]
                ]
            case "day" | "hour" | "minute":
                time_shift = timedelta(days=day, hours=hour, minutes=minute)
                patched_figure["data"][trace_idx]["x"] = pd.to_datetime(original_graph["data"][trace_idx]["x"]) + time_shift
    
        # Add transition for smooth updates
        patched_figure["layout"]["transition"] = {
            "duration": 100,  # Smooth animation over 100ms
            "easing": "linear"
        }

        return patched_figure
