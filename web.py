import streamlit as st
import requests
import os

from utils import display_map

INPUT_PATH = os.path.join('..','future_proofing_cities','data','predicted_data')
LOCAL_URL = 'http://localhost:8000/predict_city'
#
CLOUD_URL = ''

CITIES = ['Berlin','Paris']# 'Brussels', 'London'


### Streamlit app ###

# title
st.title('Predicted heat distribution')

# description
st.text('This is a web app to allow find heat islands in different cities')

# cities to select
city = st.selectbox("Type input city", CITIES)

# GET request runs prediction in background and exports geojson
params ={'city': city}
response = requests.get(LOCAL_URL, params=params)

# display map
display_map(response=response)
