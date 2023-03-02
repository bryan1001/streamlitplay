import streamlit as st
import folium
from streamlit_folium import st_folium
from locations import get_location_lat_lon, get_restaurant_near_location, add_restaurant_marker_to_map

st.set_page_config(layout="wide")

st.title("Popular Fast Food Restaurants Near Me")

# Define the list of popular fast food restaurants
restaurants = ["McDonald's", "Burger King", "Subway", "KFC", "Taco Bell", "Wendy's", "Pizza Hut", "Dunkin'", "Starbucks", "Domino's"]

# Ask user for location input
location = st.sidebar.text_input("Enter a location:")

# Use Folium to create a map centered on the user's location
m = folium.Map(location=[0, 0], zoom_start=13)

if location:
    # Get latitude and longitude of user's location
    lat, lon = get_location_lat_lon(location)
    m = folium.Map(location=st.session_state.get("location",[lat,lon]), zoom_start=13)
    folium.Marker([lat, lon]).add_to(m)

    # Ask user to select a restaurant from the dropdown
    selected_restaurant = st.sidebar.selectbox("Select a restaurant", restaurants)

    # Get the list of restaurants near the location for the selected restaurant
    response = get_restaurant_near_location(lat, lon, selected_restaurant)

    if response["status"] == "OK" and len(response["results"]) > 0:
        # Add markers for all restaurants to the map
        locations = []
        for result in response["results"]:
            name = result["name"]
            if name == selected_restaurant:
                location = result["geometry"]["location"]
                lat, lon = location["lat"], location["lng"]
                tooltip = name
                locations.append((tooltip, lat, lon))
                add_restaurant_marker_to_map(m, lat, lon, tooltip)

        # Add a list of restaurant locations to the sidebar
        st.sidebar.header(f"{selected_restaurant} Locations")
        for i, loc in enumerate(locations):
            st.sidebar.write(f"{i+1}. {loc[0]}")
            if st.sidebar.button(f"Center on {i+1}"):
                m.location = [loc[1], loc[2]]
                st.session_state["location"] = m.location
    else:
        st.warning(f"No {selected_restaurant} found within 5km of the location.")

st_folium(m, width=700, height=700)
