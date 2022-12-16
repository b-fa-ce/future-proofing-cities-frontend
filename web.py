import streamlit as st
from streamlit_folium import st_folium

from utils import display_map, get_request

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
city = st.selectbox("Select your city", ('Berlin','Paris'))
print(city)

# API GET request
response= get_request(city)

# display map
map = display_map(response=response)
st_map = st_folium(map, width=700, height=500)
