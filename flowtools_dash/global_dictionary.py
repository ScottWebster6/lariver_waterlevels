#Global Dictionary to store constants. 
#As of 1/7/2025 release, we will have to input these manually. 
#In the future, it would be ideal to have functions in this file to automate
#the getting and setting of these dictionary entries based on data passed in. 

import figures as figs

#Global Graph Dictionary
#Holds important data for all graphs used. The main key to this dictionary is used as "value" for the
#SegmentedControl component within flowtools.py. We store it here to avoid circular imports, and to let 
#us make callbacks without much fuss. 
global_graph_dictionary = {
    "stage_x_flow":{
        "func": figs.stage_x_discharge_wrapper,
        "traces_metadata_from_name":{
            "LAG Upstream Height": (0, "Height (in)"),
            "LAG Downstream Height": (1, "Height (in)"),
            "Frogspot Height" : (2, "Height (in)"),
            "Oros Height" : (3, "Height (in)"), 
            "Sepulveda Height" : (4, "Height (in)"),
            "Sepulveda Discharge": (5, "Flow (cfs)"),
        }
    },
    "temperature":{
        "func":figs.temperature_wrapper,
        "traces_metadata_from_name" : {
            "LAG Upstream Temperature" : (0, "Temperature (F)"),
            "LAG Downstream Temperature" : (1, "Temperature (F)"),
            "Frogspot Temperature" : (2, "Temperature (F)"),
            "Oros Temperature" : (3, "Temperature (F)"),
        }
    }
}

#Trace Slider Presets
#Every trace should have its own presets for its sliders, depending on what type it is. Simple!
trace_slider_presets = {
    "Height (in)" : {
        "min" : -5,
        "max" : 5,
        "step" : 0.25
    },
    
    "Temperature (F)" : {
        "min" : -20,
        "max" : 20,
        "step" : 1
    },
    
    "Flow (cfs)" : {
        "min" : -60,
        "max" : 60,
        "step" : 10
    },
    
    "Flow (MGD)" : {
        "min" : -10,
        "max" : 10,
        "step" : 1
    }
}
