import numpy as np
import folium
import geopandas
import streamlit as st
import requests
from streamlit_folium import st_folium
import branca.colormap as cmp
import json, os

CITIES = ['Paris','Berlin']
CITY_CENTER = {'Paris': [48.864716, 2.349014], 'Berlin': [52.5200, 13.4050]}

INPUT_PATH = os.path.join('..','future_proofing_cities','data','predicted_data')
LOCAL_URL = 'http://localhost:8000/predict_city'
#
CLOUD_URL = ''


def linear_cm(lst_min, lst_max):
    linear = cmp.LinearColormap(
        ['blue', 'white', 'red'],
        vmin=lst_min, vmax=lst_max,
        caption='ΔT[°C]' #Caption for Color scale or Legend
    )
    return linear


def display_map(response: dict):
    """"
    display map for API response
    """
    json_response = response.json()
    city = json_response['city']

    # read gdf
    gdf = geopandas.read_file(json_response['gdf'], driver = 'GeoJSON', dtypes = 'float64')
    gdf['id'] = gdf['id'].astype('int')

    geo_json = json.loads(json_response['gdf'])

    map = folium.Map(location=CITY_CENTER[city],
                     zoom_start=12,
                     scrollWheelZoom=True,
                     tiles='Stamen Terrain',
                     width=750,
                     height=500)
                    #  crs = 'EPSG4326')#'CartoDB positron')


    # linear cmap
    linear = linear_cm(min(gdf['LST_diff']), np.quantile(gdf['LST_diff'],.9))



    for iteration, row in gdf.iterrows():

        geo = geopandas.GeoSeries(row['geometry'])
        heat_value = row['LST_diff']

        geo_json = geo.to_json()

        choropleth = folium.GeoJson(
                    geo_json,
                    style_function=lambda x, heat_value = heat_value:
                        {'weight': .2,
                        'color': 'gray',
                        'dashArray': '5, 3',
                        'fillColor': linear(heat_value)}

                    )

        choropleth.add_to(map)

        folium.Popup(f'ΔT[°C]" = ' + str(round(row['LST_diff'],3)), max_width=1000).add_to(choropleth)


    linear.add_to(map)

      # full scree mode option
    folium.plugins.Fullscreen(position='topleft').add_to(map)

    return map
    # st_map = st_folium(map, width=700, height=500)

# GET request runs prediction in background and exports geojson
@st.cache
def get_request(city: str):
    """
    GET request runs prediction in background and exports geojson
    """
    params ={'city': city}
    response = requests.get(LOCAL_URL, params=params)
    return response
