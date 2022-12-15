import streamlit as st
import requests
import geopandas
import pandas as pd
from folium import plugins
import folium
from streamlit_folium import st_folium
# from shapely.geometry import shape
import numpy as np
# from shapely.geometry import Polygon
from branca.colormap import linear
import branca.colormap as cmp
import os

INPUT_PATH = os.path.join('..','future_proofing_cities','data','predicted_data')
LOCAL_URL = 'http://localhost:8888/predict_city'
#
CLOUD_URL = ''

### Streamlit app ###

# title
st.title('Predicted heat distribution')

# description
st.text('This is a web app to allow find heat islands in different cities')

# cities to select
city = st.selectbox("Type input city", ['Paris','Berlin']) # 'Brussels', 'London',

# GET request runs prediction in background and exports geojson
params ={'city': city}
response = requests.get(LOCAL_URL, params=params)

# import geojson
in_path = os.path.join(INPUT_PATH, city, f'{city}_viz.geojson')
df = geopandas.read_file(in_path)

# map locations -> update here
if city == 'Paris':
    map = folium.Map(location=[48.864716, 2.349014],
                     width =1000,
                    height=500,
                     zoom_start=13,
                     tiles='CartoDB positron',
                     control_scale=True,
                     )
else:
    map = folium.Map(location=[52.5200, 13.4050],
                     zoom_start=15,
                     tiles = 'CartoDB positron',
                     control_scale=True)

def getting_min_max():
    data_n = df[['LST_diff']]
    min_number = data_n.min()
    max_number = data_n.max()
    min_number = min_number.item()
    max_number = max_number.item()
    return  min_number, max_number


# update to more colors in range of T
def map_color(heat):
    # print(getting_max_min())
    global min_lst, max_lst, n
    if min_lst < heat < min_lst + n:
        return '#080cfc'
    elif min_lst + n <= heat < min_lst + 2 * n:
        return '#b8cffc'
    elif min_lst + 2 * n <= heat < min_lst + 3 * n:
        return '#fcce58'
    elif min_lst + 3 * n <= heat < min_lst + 4 * n:
        return '#b8e2fc'
    else:
        return '#ff0000'


min_lst, max_lst = getting_min_max()
n = (max_lst - min_lst) / 5
# add tiles to map
for iteration, r in df.iterrows():
    sim_geo = geopandas.GeoSeries(r['geometry']).simplify(tolerance=0.002)
    heat_value = r['LST_diff']
    geo_j = sim_geo.to_json()
    geo_j = folium.GeoJson(data=geo_j,
                        style_function=lambda x,
                        heat_value=heat_value: {'fillColor': map_color(heat_value)})

    folium.Popup(r['LST_diff']).add_to(geo_j)
    geo_j.add_to(map)


# full scree mode option
plugins.Fullscreen(position='topright').add_to(map)

# add legend -> update
step = cmp.StepColormap(
 ['#080cfc', '#b8cffc', '#fcce58', '#b8e2fc', '#ff0000'],
 vmin=min_lst, vmax=max_lst,
 index=[min_lst, min_lst + 2 * n, min_lst + 3 * n, min_lst + 4 * n, max_lst],  #for change in the colors, not used fr linear
 caption='Color Scale for Map'    #Caption for Color scale or Legend
)
# step
step.add_to(map)

# print map on website
st_folium(map)

# add balloons)
st.balloons()
