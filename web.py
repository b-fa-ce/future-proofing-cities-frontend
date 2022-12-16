import streamlit as st
from streamlit_folium import st_folium
from PIL import Image

from utils import display_map, get_request, get_city

LOCAL_URL = 'http://localhost:8000/predict_city'
#
CLOUD_URL = ''

CITIES = ['Berlin','Paris']# 'Brussels', 'London'

### Streamlit app ###

# title
st.title('Predicted heat distribution')

# description
st.text('Heat distributions in different cities with respect to the mean city temperature')

with st.sidebar:

    logo = Image.open('images/fpc_logo.png')
    st.image(logo)


    st.subheader('Future proofing cities')
    st.write('A two week project at Le Wagon\'s Data Science & Machine Learning bootcamp')
    st.write('#')

    col1, col2 = st.columns([1,7])
    with col1:
        gh_logo = Image.open('images/github.png')
        st.image(gh_logo,width=30)
    with col2:
        st.markdown('**[GitHub repository](https://github.com/b-fa-ce/future_proofing_cities)**')


    st.write('#')

    st.markdown('**:blue[Contributors]**:')
    st.write('Afanasis Kiurdzhyiev')
    st.write('Matt Hall')
    st.write('Leah Rothschild')
    st.write('Bruno Faigle-Cedzich')




with st.container():
    # cities to select
    input = st.selectbox("Select your city", (CITIES))

    city = get_city(input)
    print(city)

    # API GET request
    response= get_request(city)

    # display map
    map = display_map(response=response)
    st_map = st_folium(map, width=700, height=500)
