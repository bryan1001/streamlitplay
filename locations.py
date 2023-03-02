import streamlit as st

import requests
from geopy import Nominatim
import folium


@st.cache_data
def get_location_lat_lon(location):
    geocode = Nominatim(user_agent="myapp").geocode(location)
    return geocode.latitude, geocode.longitude

@st.cache_data
def get_restaurant_near_location(lat, lon, selected_restaurant):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{lat},{lon}",
        "radius": 5000,  # search within a 5km radius
        "type": "restaurant",
        "keyword": selected_restaurant,
        "key": st.secrets["google_places_api_key"]
    }
    response = requests.get(url, params=params).json()
    return response


def add_restaurant_marker_to_map(m, lat, lon, tooltip):
    icon = folium.features.CustomIcon('https://upload.wikimedia.org/wikipedia/commons/3/36/McDonald%27s_Golden_Arches.svg', icon_size=(20, 20))
    # Add a black rounded-rect background to the marker icon
    div_icon = folium.features.DivIcon(
        icon_size=(36, 36),
        icon_anchor=(18, 12),
        html=f'<div style="background-color: black; border-radius: 8px; padding: 4px;">{tooltip}</div>'
    )
    folium.Marker([lat, lon], tooltip=tooltip, icon=div_icon).add_to(m)
    folium.Marker([lat, lon], tooltip=tooltip, icon=icon, icon_offset=(0, -15)).add_to(m)
