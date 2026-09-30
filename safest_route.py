import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
import pandas as pd
import time
import math
import os

def run_safest_route():

    st.set_page_config(layout="wide")
    st.title("🚺 StreeTranam - Smart Safest Route")

    # -------- LOAD DATASET (LOCAL FILE) --------
    FILE_PATH = "safety_data.csv"

    if not os.path.exists(FILE_PATH):
        st.error("❌ Dataset file not found. Make sure 'safety_data.csv' is in this folder.")
        st.stop()

    df = pd.read_csv(FILE_PATH)

    # -------- CLEAN DATA --------
    risk_map = {"low": 1, "medium": 5, "high": 10}
    df["risk_score"] = df["risk_level"].str.lower().map(risk_map)

    # -------- SESSION STATE --------
    if "route_data" not in st.session_state:
        st.session_state.route_data = None

    # -------- INPUT --------
    start = st.text_input("Enter Start Location", "Charminar, Hyderabad")
    end = st.text_input("Enter Destination", "Koti, Hyderabad")

    # -------- GET COORDS --------
    @st.cache_data
    def get_coords(place):
        url = "https://nominatim.openstreetmap.org/search"
        params = {"q": place, "format": "json"}
        headers = {"User-Agent": "StreeTranamApp"}

        try:
            response = requests.get(url, params=params, headers=headers)
            data = response.json()

            if len(data) == 0:
                return None

            return float(data[0]['lat']), float(data[0]['lon'])
        except:
            return None

    # -------- DISTANCE --------
    def distance(a, b):
        return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

    # -------- PRECOMPUTE AREA COORDS --------
    @st.cache_data
    def prepare_area_coords(df):
        coords = []
        for _, row in df.iterrows():
            loc = get_coords(row["area_name"] + ", Hyderabad")
            if loc:
                coords.append((loc[0], loc[1], row["risk_score"]))
        return coords

    area_coords = prepare_area_coords(df)

    # -------- GET RISK --------
    def get_risk(lat, lon):
        min_dist = float("inf")
        risk = 1

        for alat, alon, arisk in area_coords:
            d = distance((lat, lon), (alat, alon))
            if d < min_dist:
                min_dist = d
                risk = arisk

        return risk

    # -------- GET ROUTE --------
    def get_route(start_coords, end_coords):
        url = f"http://router.project-osrm.org/route/v1/driving/{start_coords[1]},{start_coords[0]};{end_coords[1]},{end_coords[0]}?overview=full&geometries=geojson"

        try:
            response = requests.get(url)
            data = response.json()

            if "routes" not in data:
                return None, None, None

            route = data["routes"][0]

            coords = [(lat, lon) for lon, lat in route["geometry"]["coordinates"]]
            distance_km = route["distance"] / 1000
            time_min = route["duration"] / 60

            return coords, distance_km, time_min
        except:
            return None, None, None

    # -------- BUTTON --------
    if st.button("Find Safest Route"):

        st.session_state.route_data = None

        with st.spinner("🔍 Finding safest route..."):
            time.sleep(1)

            start_coords = get_coords(start)
            end_coords = get_coords(end)

            if not start_coords or not end_coords:
                st.error("Invalid locations")
                st.stop()

            route_coords, dist, dur = get_route(start_coords, end_coords)

            if route_coords is None:
                st.error("Route not found")
                st.stop()

            st.session_state.route_data = {
                "coords": route_coords,
                "start": start_coords,
                "end": end_coords,
                "distance": dist,
                "duration": dur,
                "start_name": start,
                "end_name": end
            }

    # -------- DISPLAY --------
    if st.session_state.route_data:

        data = st.session_state.route_data

        center = [
            (data["start"][0] + data["end"][0]) / 2,
            (data["start"][1] + data["end"][1]) / 2
        ]

        m = folium.Map(location=center, zoom_start=12, tiles="cartodbpositron")

        # -------- DRAW ROUTE WITH RISK --------
        for i in range(len(data["coords"]) - 1):
            p1 = data["coords"][i]
            p2 = data["coords"][i + 1]

            risk = get_risk(p1[0], p1[1])

            if risk >= 8:
                color = "red"
            elif risk >= 4:
                color = "orange"
            else:
                color = "green"

            folium.PolyLine([p1, p2], color=color, weight=6).add_to(m)

        # Markers
        folium.Marker(
            data["start"],
            tooltip=f"Start: {data['start_name']}",
            icon=folium.Icon(color="green")
        ).add_to(m)

        folium.Marker(
            data["end"],
            tooltip=f"End: {data['end_name']}",
            icon=folium.Icon(color="red")
        ).add_to(m)

        st_folium(m, width=1000, height=550)

        # -------- METRICS --------
        col1, col2 = st.columns(2)

        col1.metric("📏 Distance", f"{data['distance']:.2f} km")
        col2.metric("⏱️ Time", f"{data['duration']:.1f} mins")

        st.success("✅ Route generated using built-in safety dataset!")


if __name__ == "__main__":
    run_safest_route()
