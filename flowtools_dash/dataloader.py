import numpy as np
import pandas as pd
import plotly.express as px
import requests
from datetime import date, datetime, timedelta

#local
from cache import cache


#1/7/2024 Release:
#For now, data must be inputted from HoboWare to the GitHub repository manually. 
#A GUI tool to handle this should be made in the future, if time allows. 

#Constants
START_DATE = '9-23-2024 19:00:00'
END_DATE = '12-15-2024 15:10:00'
TIMEOUT = 300

#Returns flow data from DCT and LAG plants
def getlasan(url: str) -> pd.DataFrame:
    temp = pd.read_excel(url)
    temp.rename(columns={'Date Time':'Datetime'}, inplace=True)
    temp.rename(columns={'LAG Effluent ':'LAG Effluent (MGD)'}, inplace=True)
    temp['Datetime'] = pd.to_datetime(temp['Datetime'], format='%m/%d/%y %I:%M:%S %p')
    return temp

# Returns data from csv files exported from Hoboware and makes necessary format changes
def getdata(url: str) -> pd.DataFrame:
    temp = pd.read_csv(url)
    temp.drop('#', axis=1, inplace=True)
    temp.columns = ['Datetime', 'PSI', 'Temperature (F)', 'Height (in)']
    temp['Datetime'] = pd.to_datetime(temp['Datetime'], format='%m/%d/%y %I:%M:%S %p')
    temp['Height (in)'] = temp['Height (in)'] * 39.3700787402  # meters -> inches
    return temp


# Returns data from USGS .txt data format
def getusgsdata(url: str, units: str) -> pd.DataFrame:
    r = requests.get(url)
    r.raise_for_status()
    data = []
    for line in r.text.splitlines():
        fields = line.split()
        Datetime = fields[2] + ' ' + fields[3]
        measurement = float(fields[5])
        data.append([Datetime, measurement])
    df = pd.DataFrame(data, columns=['Datetime', units])
    df['Datetime'] = pd.to_datetime(df['Datetime'])
    return df

# Can parse datetime object or string formatted as 'YYYY MM DD"
def databyday(target_date, df: pd.DataFrame) -> pd.DataFrame:
    target_date = pd.to_datetime(target_date)
    return df[df['Datetime'].dt.date == target_date.date()]


def databyday_norm(month: int, day: int, df: pd.DataFrame) -> pd.DataFrame:
    return df[(df['Datetime'].dt.month == month) & (df['Datetime'].dt.day == day)]

# Can parse datetime object or string formatted as 'YYYY MM DD HH:MM:SS'
def databyrange(start_datetime, end_datetime, df: pd.DataFrame) -> pd.DataFrame:
    start_datetime = pd.to_datetime(start_datetime)
    end_datetime = pd.to_datetime(end_datetime)
    return df[(df['Datetime'] >= start_datetime) & (df['Datetime'] <= end_datetime)]
    
    
#Load individual dataframes and clean them appropriately.

@cache.memoize(timeout=TIMEOUT)
def load_frog_df():
    frog_url = 'https://raw.githubusercontent.com/ScottWebster6/lariver_waterlevels/refs/heads/main/Frogspot_levels_22072298_09_10_24-12_15_24_merged.csv'
    frog_df = databyrange(START_DATE, END_DATE, getdata(frog_url))
    #one frogspot reading is erroneous (Nov 1st, @ 17:45, somehow negative?)
    bad_index = frog_df[frog_df['Datetime'] == datetime(2024, 11, 1, 17, 45)].index[0]
    frog_df.at[bad_index, 'Height (in)'] = (frog_df.at[bad_index-1, 'Height (in)'] + frog_df.at[bad_index+1, 'Height (in)'])/2
    return frog_df

@cache.memoize(timeout=TIMEOUT)
def load_gla_up_df():
    gla_up_url = 'https://raw.githubusercontent.com/ScottWebster6/lariver_waterlevels/refs/heads/main/GLA_Upstream_levels_22072299_09_23_24-12_15_24.csv'
    gla_up_df = databyrange(START_DATE, END_DATE, getdata(gla_up_url))
    return gla_up_df

@cache.memoize(timeout=TIMEOUT)
def load_gla_down_df():
    gla_down_url = 'https://raw.githubusercontent.com/ScottWebster6/lariver_waterlevels/refs/heads/main/GLA_Downstream_levels_22072297_09_23_24-12_15_24.csv'
    gla_down_df = databyrange(START_DATE, END_DATE, getdata(gla_down_url))
    return gla_down_df

@cache.memoize(timeout=TIMEOUT)
def load_oros_df():
    oros_url = 'https://raw.githubusercontent.com/ScottWebster6/lariver_waterlevels/refs/heads/main/oros_levels_compensated_22072300_09_10_24-12_15_24.csv'
    oros_df = databyrange(START_DATE, END_DATE, getdata(oros_url))
    return oros_df
    
@cache.memoize(timeout=TIMEOUT)    
def load_usgs_height_df():
    usgs_height_url = 'https://raw.githubusercontent.com/ScottWebster6/lariver_waterlevels/refs/heads/main/usgs_sepulveda_stageheight.txt'
    usgs_height_df = databyrange(START_DATE, END_DATE, getusgsdata(usgs_height_url, 'Height (feet)'))
    #converting usgs data
    usgs_height_df['Height (feet)'] = usgs_height_df['Height (feet)'] * 12 #feet -> inches
    usgs_height_df.columns = ['Datetime', 'Height (in)']
    return usgs_height_df

@cache.memoize(timeout=TIMEOUT)
def load_usgs_discharge_df():
    usgs_discharge_url = 'https://raw.githubusercontent.com/ScottWebster6/lariver_waterlevels/refs/heads/main/usgs_sepulveda_discharge.txt'
    usgs_discharge_df = databyrange(START_DATE, END_DATE, getusgsdata(usgs_discharge_url, 'Flow (cfs)'))
    return usgs_discharge_df

#Load all data at once.
#Usage:
#gla_up_df, gla_down_df, frog_df, oros_df, usgs_height_df, usgs_discharge_df = dataloader.load_all_data()
#Python is weird, but most pythonic abstractions are fairly useful. 
#(don't need to cache this function because it contains caching functions!)
def load_all_data():
    
    gla_up_df = load_gla_up_df()
    gla_down_df = load_gla_down_df()
    frog_df = load_frog_df()
    oros_df = load_oros_df()
    usgs_height_df = load_usgs_height_df()
    usgs_discharge_df = load_usgs_discharge_df()
    
    return gla_up_df, gla_down_df, frog_df, oros_df, usgs_height_df, usgs_discharge_df