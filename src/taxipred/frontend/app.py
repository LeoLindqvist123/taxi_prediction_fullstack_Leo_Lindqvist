# Have used chatgpt for my frontend to understand better and have nicer look 

import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Taxi Price Predictor", page_icon="🚕")

API_URL = "http://127.0.0.1:8000/api/taxi/v1"

st.title("🚕 Taxi Price Predictor")
st.write("Predicera taxipriser baserat på resedetaljer")

st.sidebar.header("Rese-information")

trip_distance = st.sidebar.number_input("Avstånd (km)", min_value=0.1, max_value=100.0, value=10.0, step=0.1)
time_of_day = st.sidebar.selectbox("Tid på dagen", ["Morning", "Afternoon", "Evening", "Night"])
day_of_week = st.sidebar.selectbox("Veckodag", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
passenger_count = st.sidebar.slider("Antal passagerare", 1, 8, 2)
traffic_conditions = st.sidebar.selectbox("Trafik", ["Light", "Medium", "Heavy"])
weather = st.sidebar.selectbox("Väder", ["Clear", "Rainy", "Cloudy", "Snowy"])
base_fare = st.sidebar.number_input("Baspris", min_value=0.0, value=50.0, step=1.0)
per_km_rate = st.sidebar.number_input("Pris per km", min_value=0.0, value=10.0, step=0.5)
per_minute_rate = st.sidebar.number_input("Pris per minut", min_value=0.0, value=2.0, step=0.1)
trip_duration = st.sidebar.number_input("Restid (minuter)", min_value=0.1, value=25.0, step=0.5)

if st.sidebar.button("Predicera Pris", type="primary"):

    payload = {
        "Trip_Distance_km": trip_distance,
        "Time_of_Day": time_of_day,
        "Day_of_Week": day_of_week,
        "Passenger_Count": passenger_count,
        "traffic_conditions": traffic_conditions,
        "Weather": weather,
        "Base_Fare": base_fare,
        "Per_Km_Rate": per_km_rate,
        "Per_Minute_Rate": per_minute_rate,
        "Trip_Duration_Minutes": trip_duration
    }
    
    try:
        response = requests.post(f"{API_URL}/predict", json=payload)
        
        if response.status_code == 200:
            result = response.json()
            predicted_price = result["predicted_price"]
            
            st.success(f"💰 Predicerat pris: **{predicted_price:.2f} kr**")
            
            st.subheader("Resedetaljer")
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Avstånd", f"{trip_distance} km")
                st.metric("Passagerare", passenger_count)
                st.metric("Restid", f"{trip_duration} min")
            
            with col2:
                st.metric("Tid", time_of_day)
                st.metric("Trafik", traffic_conditions)
                st.metric("Väder", weather)
        else:
            st.error(f"Fel: {response.status_code} - {response.text}")
    
    except Exception as e:
        st.error(f"Kunde inte ansluta till API: {e}")
        st.info("Se till att FastAPI-servern körs på http://127.0.0.1:8000")

st.divider()
if st.checkbox("Visa all taxi-data"):
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True)
        else:
            st.error("Kunde inte hämta data")
    except Exception as e:
        st.error(f"Fel: {e}")