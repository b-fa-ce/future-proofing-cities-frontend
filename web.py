import streamlit as st
# import json
import requests
import geopandas
# import pyproj
# import plotly.graph_objs as go
# import pandas as pd
from folium import plugins
# from folium.plugins import HeatMap
import folium
from streamlit_folium import st_folium
# import fiona
# from shapely.geometry import shape
import numpy as np
# from shapely.geometry import Polygon
from branca.colormap import linear

import os

INPUT_PATH = os.path.join('..','future_proofing_cities','data','predicted_data')
LOCAL_URL = 'http://localhost:8888/predict_city'
CLOUD_URL = ''

### Streamlit app ###

# title
st.title('Predicted heat distribution')

# description
st.text('This is a web app to allow find heat islands in different cities')

# cities to select
city = st.selectbox("Type input city", ['Paris','Berlin']) # 'Brussels', 'London',

print(city)

# GET request runs prediction in background and exports geojson
params ={'city': city}
response = requests.get(LOCAL_URL, params=params)

# import geojson
in_path = os.path.join(INPUT_PATH, city, f'{city}_viz.geojson')
df = geopandas.read_file(in_path)

# map locations -> update here
if city == 'Paris':
    map = folium.Map(location=[48.864716, 2.349014], zoom_start=10, tiles='CartoDB positron')
elif city == 'Brussels':
    map = folium.Map(location=[50.8476, 4.3572], tiles = 'CartoDB positron', zoom_start=10, max_val=5.0, control_scale=True)
elif city == 'London':
    map = folium.Map(location=[51.5072, 0.1276], tiles = 'CartoDB positron', zoom_start=10, max_val=5.0, control_scale=True)
else:
    map = folium.Map(location=[52.5200, 13.4050], tiles = 'CartoDB positron', zoom_start=10, max_val=5.0, control_scale=True)


# update to more colors in range of T
def map_color(heat):
    if -0.95 < heat < -0.5:
        return '#076cf5'
    elif -0.5 <= heat < 0:
        return '#4d97fa'
    elif 0 <= heat < 0.5:
        return '#fcce58'
    elif 0.5 <= heat < 1:
        return '#fca558'
    elif 1 <= heat < 1.5:
        return '#fa6220'
    else:
        return '#f70505'

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

# add legend -> update
count_colormap = linear.RdBu_09.scale(min(df['LST_diff']),
                                            max(df['LST_diff']))
count_colormap.add_to(map)

# full scree mode option
plugins.Fullscreen(position='topright').add_to(map)

# print map on website
st_folium(map)
