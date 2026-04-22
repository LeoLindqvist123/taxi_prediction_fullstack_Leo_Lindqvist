import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
from math import radians, cos, sin, asin, sqrt
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(page_title="Taxi Price Predictor", page_icon="🚕", layout="wide")

API_URL = os.environ.get("API_URL", "http://127.0.0.1:8000") + "/api/taxi/v1"
GEOAPIFY_KEY = os.environ.get("GEOAPIFY_API_KEY")

def geocode(address):
    url = f"https://api.geoapify.com/v1/geocode/search?text={address}&apiKey={GEOAPIFY_KEY}"
    r = requests.get(url)
    data = r.json()
    if data['features']:
        coords = data['features'][0]['geometry']['coordinates']
        return coords[1], coords[0]  # lat, lon
    return None, None

st.title("🚕 Taxi Price Predictor")
st.caption("Enter your starting and ending destination to get a price estimate..")
st.divider()

st.sidebar.header("🗺️ Travel information")
start = st.sidebar.text_input("Start address", "Stockholm Central")
slut = st.sidebar.text_input("Final address", "Arlanda")
passengers = st.sidebar.slider("Passanges", 1, 8, 2)

st.sidebar.header("⚙️ Resedetaljer")
time_of_day = st.sidebar.selectbox("Time of the day", ["Morning", "Afternoon", "Evening", "Night"])
day_of_week = st.sidebar.selectbox("Day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
weather = st.sidebar.selectbox("Weather", ["Clear", "Rainy", "Snowy", "Foggy"])
traffic = st.sidebar.selectbox("Trafic", ["Low", "Medium", "High"])

calculate = st.sidebar.button("🚕 Beräkna pris", type="primary", use_container_width=True)

if calculate:
    st.session_state['run_calculation'] = True

if 'run_calculation' in st.session_state and st.session_state['run_calculation']:

    st.write("Hämtar koordinater...")

    try:
        start_lat, start_lon = geocode(start)
        slut_lat, slut_lon = geocode(slut)

        if not start_lat or not slut_lat:
            st.error("❌ Could not find one or both addresses.")
        else:
            col_map, col_info = st.columns([2, 1])

            with col_map:
                st.subheader("🗺️ Rutt")
                m = folium.Map(
                    location=[(start_lat + slut_lat) / 2,
                               (start_lon + slut_lon) / 2],
                    zoom_start=10
                )
                folium.Marker(
                    [start_lat, start_lon],
                    popup="Start", tooltip="Start",
                    icon=folium.Icon(color='green', icon='play')
                ).add_to(m)
                folium.Marker(
                    [slut_lat, slut_lon],
                    popup="Slut", tooltip="Slut",
                    icon=folium.Icon(color='red', icon='stop')
                ).add_to(m)
                st_folium(m, width=700, height=400)

            with col_info:
                lat1, lon1 = radians(start_lat), radians(start_lon)
                lat2, lon2 = radians(slut_lat), radians(slut_lon)
                dlat, dlon = lat2 - lat1, lon2 - lon1
                a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
                dist = 6371 * 2 * asin(sqrt(a))
                tid = dist / 60 * 60

                st.subheader("📊 Reseinfo")
                st.metric("Avstånd", f"{dist:.1f} km")
                st.metric("Estimerad tid", f"{tid:.0f} min")
                st.metric("Passagerare", passengers)
                st.divider()

                try:
                    payload = {
                        "Trip_Distance_km": dist,
                        "Time_of_Day": time_of_day,
                        "Day_of_Week": day_of_week,
                        "Passenger_Count": passengers,
                        "traffic_conditions": traffic,
                        "Weather": weather,
                        "Base_Fare": 50.0,
                        "Per_Km_Rate": 10.0,
                        "Per_Minute_Rate": 2.0,
                        "Trip_Duration_Minutes": tid
                    }

                    response = requests.post(f"{API_URL}/predict", json=payload)

                    if response.status_code == 200:
                        pris = response.json()["predicted_price"]
                        st.success("### 💰 Estimated price")
                        st.metric("Pris", f"{pris:.2f} kr")
                    else:
                        st.error(f"❌ Backend error: {response.status_code} - {response.text}")

                except Exception as e:
                    st.error(f"❌ Could not reach backend: {e}")

    except Exception as e:
        st.error(f"❌ Error: {e}")