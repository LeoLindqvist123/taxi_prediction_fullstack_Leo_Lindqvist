# Have used chatgpt for my frontend to understand better and have nicer look. 

import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
import time

st.set_page_config(page_title="Taxi Price Predictor", page_icon="🚕")

API_URL = "http://127.0.0.1:8000/api/taxi/v1"

st.title("🚕 Taxi Price Predictor")

st.sidebar.header("Reseinformation")
start = st.sidebar.text_input("Start", "Stockholm Central")
slut = st.sidebar.text_input("Slut", "Arlanda")
passengers = st.sidebar.slider("Passagerare", 1, 8, 2)

if st.sidebar.button("Beräkna", type="primary"):
    st.session_state['run_calculation'] = True

if 'run_calculation' in st.session_state and st.session_state['run_calculation']:
    
        with st.spinner("Beräknar..."):

            geo = Nominatim(user_agent="taxi", timeout=10)
            start_loc = geo.geocode(start)
            time.sleep(1) 
            slut_loc = geo.geocode(slut)
            
            if not start_loc or not slut_loc:
                    st.error("Kunde inte hitta adresserna")
            else:
                    st.subheader("Rutt")
                    m = folium.Map(
                        location=[(start_loc.latitude + slut_loc.latitude)/2, 
                                  (start_loc.longitude + slut_loc.longitude)/2], 
                        zoom_start=10
                    )
                    folium.Marker([start_loc.latitude, start_loc.longitude], 
                                 popup="Start", icon=folium.Icon(color='green')).add_to(m)
                    folium.Marker([slut_loc.latitude, slut_loc.longitude], 
                                 popup="Slut", icon=folium.Icon(color='red')).add_to(m)
                    st_folium(m, width=700, height=400)

                    from math import radians, cos, sin, asin, sqrt
                    
                    lat1 = radians(start_loc.latitude)
                    lon1 = radians(start_loc.longitude)
                    lat2 = radians(slut_loc.latitude)
                    lon2 = radians(slut_loc.longitude)
                    
                    dlat = lat2 - lat1
                    dlon = lon2 - lon1
                    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
                    c = 2 * asin(sqrt(a))
                    dist = 6371 * c
                    
                    tid = dist / 60 * 60
                    
                    col1, col2 = st.columns(2)
                    col1.metric("Avstånd", f"{dist:.1f} km")
                    col2.metric("Tid", f"{tid:.0f} min")
                    
                    payload = {
                        "Trip_Distance_km": dist,
                        "Time_of_Day": "Morning",
                        "Day_of_Week": "Monday",
                        "Passenger_Count": passengers,
                        "traffic_conditions": "Medium",
                        "Weather": "Clear",
                        "Base_Fare": 50.0,
                        "Per_Km_Rate": 10.0,
                        "Per_Minute_Rate": 2.0,
                        "Trip_Duration_Minutes": tid
                    }
                    
                    response = requests.post(f"{API_URL}/predict", json=payload)
                    
                    if response.status_code == 200:
                        pris = response.json()["predicted_price"]
                        st.success(f"## Pris: {pris:.2f} kr")
                    else:
                        st.error("Kunde inte beräkna pris")