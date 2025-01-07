#Defines Plotly figures loaded into callback logic. 

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dataloader as dl

 
palette = px.colors.qualitative
colors = palette.Plotly



def stage_x_discharge(gla_up_df, gla_down_df, frog_df, oros_df, usgs_height_df, usgs_discharge_df):
        
    glauptrace_stage = go.Scatter(
        x = gla_up_df['Datetime'],
        y = gla_up_df['Height (in)'],
        mode='lines',
        name = 'LAG Upstream Stage',
        legendgroup='LAG Upstream',
        opacity=0.75,
        line=dict(color=colors[0])
    )

    gladowntrace_stage = go.Scatter(
        x = gla_down_df['Datetime'],
        y = gla_down_df['Height (in)'],
        mode='lines',
        name = 'LAG Downstream Stage',
        legendgroup='LAG Downstream',
        opacity=0.75,
        line=dict(color=colors[1])
    )

    frogtrace_stage = go.Scatter(
        x = frog_df['Datetime'],
        y = frog_df['Height (in)'],
        mode='lines',
        name = 'Frogspot Stage',
        legendgroup='Frogspot',
        opacity=0.75,
        line=dict(color=colors[2])
    )
    orostrace_stage = go.Scatter(
        x = oros_df['Datetime'],
        y = oros_df['Height (in)'],
        mode='lines',
        name = 'Oros Stage',
        legendgroup = 'Oros',
        opacity=0.75,
        line=dict(color=colors[3])
    )

    sepulveda_stage = go.Scatter(
        x = usgs_height_df['Datetime'],
        y = usgs_height_df['Height (in)'],
        mode='lines',
        name = 'Sepulveda Dam Stage',
        legendgroup = 'Sepulveda Dam',
        opacity=0.8,
        line=dict(color=colors[4])
    )

    sepulveda_discharge = go.Scatter(
        x = usgs_discharge_df['Datetime'],
        y = usgs_discharge_df['Flow (cfs)'],
        mode='lines',
        name = 'Sepulveda Dam Discharge',
        legendgroup = 'Sepulveda Dam Discharge',
        opacity=0.8,
        line=dict(color=colors[5])
    )


    fig = make_subplots(
                    # Create figure with secondary y-axis
                    specs=[[{"secondary_y": True}]]
    )
    
    fig.update_layout(
        title="LAG Stage and Flow",
        xaxis_title="Date-Time",
        yaxis=dict(title_text="<b>Stage Height</b> (in)", scaleanchor="y2"),
        yaxis2=dict(title_text="<b>Flow Rate</b> (cfs)", overlaying="y", side="right", matches="y", type='log'),
        autosize=False,
        height=768,
        width=1024,
        xaxis=dict(scaleanchor="y"),  # Locks the x-axis to the y-axis for aspect ratio
        legend_title_text="Source Toggle",
        legend=dict(
        x=1.4,  # x position slightly outside the plot
        y=1,
        xanchor="right",
        yanchor="top"
        ),
        template="none"
    )
    
    fig.add_trace(glauptrace_stage, secondary_y=False)
    fig.add_trace(gladowntrace_stage, secondary_y=False)
    fig.add_trace(frogtrace_stage, secondary_y=False)
    fig.add_trace(orostrace_stage, secondary_y=False)
    fig.add_trace(sepulveda_stage, secondary_y=False)
    fig.add_trace(sepulveda_discharge, secondary_y=True)
    
    return fig

#So that we can store the function within the Global Graph Dictionary
def stage_x_discharge_wrapper():
    #using unpack operator *
    return stage_x_discharge(*dl.load_all_data())

def temperature(gla_up_df, gla_down_df, frog_df, oros_df):
    glauptrace_temp = go.Scatter(
    x = gla_up_df['Datetime'],
    y = gla_up_df['Temperature (F)'],
    mode='lines',
    name = 'LAG Upstream Temp',
    #legendgroup='LAG Upstream',
    #opacity=1,
    showlegend=True,
    line=dict(
            color=colors[0],
            #dash='dash'
        )
    )
    gladowntrace_temp = go.Scatter(
        x = gla_down_df['Datetime'],
        y = gla_down_df['Temperature (F)'],
        mode='lines',
        name = 'LAG Downstream',
        #legendgroup = 'LAG Downstream',
        showlegend=True,
        #opacity=1,
        line=dict(
                color=colors[1],
                #dash='dash'
            )
    )


    frogtrace_temp = go.Scatter(
        x = frog_df['Datetime'],
        y = frog_df['Temperature (F)'],
        mode='lines',
        name = "Frogspot Temp",
        #legendgroup='Frogspot',
        showlegend=True,
        #opacity=1,
        line=dict(
                color=colors[2],
                # dash='dash'
            )
    )

    orostrace_temp = go.Scatter(
        x = oros_df['Datetime'],
        y = oros_df['Temperature (F)'],
        mode='lines',
        #marker=dict(
        #           symbol="circle-dot",
        #           size=5,
                    #angleref="previous",
        #      ),
        name = 'Oros Temp',
        #legendgroup = 'Oros',
        showlegend=True,
        opacity=1,
        line=dict(
                color=colors[3],
                # dash='dash'
            )
    )
    fig = go.Figure(
        data = [glauptrace_temp, gladowntrace_temp, frogtrace_temp, orostrace_temp],
        layout= go.Layout(
            title="LA River Temperature",
            #xaxis_title="Date-Time",
            autosize=False,
            height=768,     # 4:3 aspect ratio for each graph
            width=1024,
            yaxis=dict(title_text="<b>Temperature</b> (F)"),
            xaxis=dict(title_text= "<b>Date-Time</b>", scaleanchor="y"),  # Locks the x-axis to the y-axis for aspect ratio
            legend=dict(
                        #groupclick="toggleitem",
                        title_text="Source Toggle",
                        x=1.4,  # x position slightly outside the plot
                        y=1,
                        xanchor="right",
                        yanchor="top"),
            template="none"
        )
    )
    return fig

#So that we can store the function within the Global Graph Dictionary

def temperature_wrapper():
    return temperature(dl.load_gla_up_df(), dl.load_gla_down_df(), dl.load_frog_df(), dl.load_oros_df())


