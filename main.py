import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import random
import folium
from streamlit_folium import st_folium
from sklearn.cluster import KMeans
import mysql.connector


# Page Configuration
st.set_page_config(
    page_title="StreeTranam - Safety First",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme with rose/coral accents
st.markdown("""
<style>
    /* Main theme */
    .stApp {
        background: linear-gradient(135deg, #1a1625 0%, #1e1a2e 100%);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #13111c 0%, #1a1625 100%);
        border-right: 1px solid #2d2640;
    }
    
    /* Cards */
    .card {
        background: linear-gradient(145deg, #231f35 0%, #1e1a2e 100%);
        border: 1px solid #2d2640;
        border-radius: 16px;
        padding: 24px;
        margin: 10px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .card-header {
        color: #f0e6ff;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    /* Primary button */
    .primary-btn {
        background: linear-gradient(135deg, #e85a8f 0%, #d64577 100%);
        color: white;
        padding: 12px 24px;
        border-radius: 12px;
        border: none;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        text-align: center;
        display: inline-block;
    }
    
    .primary-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(232, 90, 143, 0.4);
    }
    
    /* SOS Button */
    .sos-button {
        background: linear-gradient(135deg, #ff4757 0%, #ff3344 100%);
        color: white;
        padding: 20px 40px;
        border-radius: 50px;
        font-size: 1.5rem;
        font-weight: 700;
        text-align: center;
        cursor: pointer;
        animation: pulse 2s infinite;
        box-shadow: 0 0 40px rgba(255, 71, 87, 0.5);
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 20px rgba(255, 71, 87, 0.5); }
        50% { box-shadow: 0 0 40px rgba(255, 71, 87, 0.8); }
        100% { box-shadow: 0 0 20px rgba(255, 71, 87, 0.5); }
    }
    
    /* Safe indicator */
    .safe-indicator {
        background: linear-gradient(135deg, #2ed573 0%, #26ab5f 100%);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
    }
    
    /* Warning indicator */
    .warning-indicator {
        background: linear-gradient(135deg, #ffa502 0%, #ff8c00 100%);
        color: #1a1625;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
    }
    
    /* Metric card */
    .metric-card {
        background: linear-gradient(145deg, #2d2640 0%, #231f35 100%);
        border: 1px solid #3d3555;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #e85a8f 0%, #ff8a9b 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .metric-label {
        color: #9d95b8;
        font-size: 0.85rem;
        margin-top: 4px;
    }
    
    /* Guardian card */
    .guardian-card {
        background: linear-gradient(145deg, #2d2640 0%, #231f35 100%);
        border: 1px solid #3d3555;
        border-radius: 12px;
        padding: 16px;
        margin: 8px 0;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .guardian-avatar {
        width: 48px;
        height: 48px;
        border-radius: 50%;
        background: linear-gradient(135deg, #e85a8f 0%, #d64577 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 600;
        font-size: 1.2rem;
    }
    
    /* Status badge */
    .status-active {
        background: #2ed573;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 6px;
        animation: blink 1.5s infinite;
    }
    
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    /* Map placeholder */
    .map-container {
        background: linear-gradient(145deg, #1e1a2e 0%, #13111c 100%);
        border: 2px solid #3d3555;
        border-radius: 16px;
        height: 400px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        position: relative;
        overflow: hidden;
    }
    
    .map-grid {
        position: absolute;
        width: 100%;
        height: 100%;
        background-image: 
            linear-gradient(rgba(61, 53, 85, 0.3) 1px, transparent 1px),
            linear-gradient(90deg, rgba(61, 53, 85, 0.3) 1px, transparent 1px);
        background-size: 40px 40px;
    }
    
    .location-marker {
        width: 20px;
        height: 20px;
        background: #e85a8f;
        border-radius: 50%;
        position: relative;
        z-index: 10;
        box-shadow: 0 0 20px rgba(232, 90, 143, 0.6);
    }
    
    .location-marker::after {
        content: '';
        position: absolute;
        width: 40px;
        height: 40px;
        border: 2px solid #e85a8f;
        border-radius: 50%;
        top: -10px;
        left: -10px;
        animation: ripple 2s infinite;
    }
    
    @keyframes ripple {
        0% { transform: scale(1); opacity: 1; }
        100% { transform: scale(2); opacity: 0; }
    }
    
    /* Trip route line */
    .route-line {
        position: absolute;
        height: 4px;
        background: linear-gradient(90deg, #2ed573, #e85a8f, #ff4757);
        border-radius: 2px;
        width: 60%;
        z-index: 5;
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        background: #231f35;
        border: 1px solid #3d3555;
        border-radius: 8px;
        color: #f0e6ff;
    }
    
    .stSelectbox > div > div {
        background: #231f35;
        border: 1px solid #3d3555;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: #231f35;
        border-radius: 8px;
        color: #9d95b8;
        border: 1px solid #3d3555;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #e85a8f 0%, #d64577 100%);
        color: white;
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #e85a8f, #ff8a9b);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: #231f35;
        border-radius: 8px;
    }
    
    /* Hide default streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Title styling */
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #e85a8f 0%, #ff8a9b 50%, #2ed573 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 8px;
    }
    
    .subtitle {
        color: #9d95b8;
        text-align: center;
        font-size: 1rem;
        margin-bottom: 24px;
    }
    
    /* Feature card */
    .feature-card {
        background: linear-gradient(145deg, #231f35 0%, #1e1a2e 100%);
        border: 1px solid #3d3555;
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
        height: 100%;
    }
    
    .feature-card:hover {
        transform: translateY(-4px);
        border-color: #e85a8f;
        box-shadow: 0 12px 40px rgba(232, 90, 143, 0.2);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 12px;
    }
    
    .feature-title {
        color: #f0e6ff;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 8px;
    }
    
    .feature-desc {
        color: #9d95b8;
        font-size: 0.85rem;
    }
    
    /* Quote card */
    .quote-card {
        background: linear-gradient(145deg, #2d2640 0%, #231f35 100%);
        border-left: 4px solid #e85a8f;
        border-radius: 0 12px 12px 0;
        padding: 20px 24px;
        margin: 16px 0;
        font-style: italic;
        color: #d4cce8;
    }
    
    .quote-author {
        color: #e85a8f;
        font-style: normal;
        font-weight: 600;
        margin-top: 12px;
        text-align: right;
    }
    
    /* Breathing circle */
    .breathing-circle {
        width: 150px;
        height: 150px;
        border-radius: 50%;
        background: linear-gradient(135deg, #4ecdc4 0%, #2ed573 100%);
        margin: 20px auto;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 600;
        animation: breathe 8s infinite ease-in-out;
    }
    
    @keyframes breathe {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.2); }
    }
    
    /* Incident severity */
    .severity-low { border-left: 4px solid #2ed573; }
    .severity-medium { border-left: 4px solid #ffa502; }
    .severity-high { border-left: 4px solid #ff4757; }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'dashboard'
if 'guardian_mode_active' not in st.session_state:
    st.session_state.guardian_mode_active = False
if 'guardians' not in st.session_state:
    st.session_state.guardians = [
        {"name": "Mom", "phone": "+91 98765 43210", "active": True},
        {"name": "Best Friend", "phone": "+91 87654 32109", "active": True},
    ]
if 'trip_active' not in st.session_state:
    st.session_state.trip_active = False
if 'check_ins' not in st.session_state:
    st.session_state.check_ins = 0
if 'safety_score' not in st.session_state:
    st.session_state.safety_score = 87
if 'incidents' not in st.session_state:
    st.session_state.incidents = []

# Sidebar Navigation
# Sidebar Navigation
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <div style="font-size: 2.5rem;">🛡️</div>
        <div class="main-title" style="font-size: 1.5rem;">StreeTranam</div>
        <div class="subtitle" style="font-size: 0.8rem; margin-bottom: 0;">
            Safety First, Always
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Navigation pages
    pages = {
        "dashboard": ("📊", "Dashboard"),
        "guardian": ("👁️", "Guardian Mode"),
        "trip": ("🗺️", "Trip Analyzer"),
        "map_page": ("🗺️", "Safety Map"),
        "emergency": ("🚨", "Emergency SOS"),
        "report": ("📝", "Report Incident"),
        "safety_form": ("📋", "Safety Form"),
        "support": ("💜", "Support & Care"),
        "settings": ("⚙️", "Settings"),
    }

    # Sidebar buttons (FIXED KEYS)
    for page_key, (icon, label) in pages.items():
        if st.button(
            f"{icon} {label}",
            key=f"sidebar_nav_{page_key}",   # ✅ UNIQUE KEY FIX
            use_container_width=True
        ):
            st.session_state.current_page = page_key
            st.rerun()

    st.markdown("---")

    # SOS Button
    st.markdown("""
    <div style="text-align: center; margin-top: 20px;">
        <div style="color: #9d95b8; font-size: 0.8rem; margin-bottom: 8px;">
            Quick Emergency
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button(
        "🚨 SOS",
        key="sidebar_sos_unique",   # ✅ UNIQUE KEY FIX
        use_container_width=True
    ):
        st.session_state.current_page = 'emergency'
        st.rerun()

# Main Content Area
def render_dashboard():
    st.markdown('<h1 class="main-title">Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Your safety overview at a glance</p>', unsafe_allow_html=True)
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{st.session_state.safety_score}%</div>
            <div class="metric-label">Safety Score</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(st.session_state.guardians)}</div>
            <div class="metric-label">Active Guardians</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{st.session_state.check_ins}</div>
            <div class="metric-label">Check-ins Today</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        guardian_status = "Active" if st.session_state.guardian_mode_active else "Inactive"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="font-size: 1.2rem;">{guardian_status}</div>
            <div class="metric-label">Guardian Mode</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Quick Actions
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="card">
            <div class="card-header">⚡ Quick Actions</div>
        </div>
        """, unsafe_allow_html=True)
        
        action_col1, action_col2 = st.columns(2)
        with action_col1:
            if st.button("🚨 Emergency SOS", use_container_width=True, type="primary"):
                st.session_state.current_page = 'emergency'
                st.rerun()
            if st.button("👁️ Start Guardian", use_container_width=True):
                st.session_state.current_page = 'guardian'
                st.rerun()
            
    # Emergency Helplines
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="card">
        <div class="card-header">📞 Emergency Helplines</div>
    </div>
    """, unsafe_allow_html=True)
    
    helpline_cols = st.columns(4)
    helplines = [
        ("🚔", "Police", "100"),
        ("🚑", "Ambulance", "102"),
        ("👩", "Women Helpline", "1091"),
        ("🆘", "Emergency", "112"),
    ]
    
    for col, (icon, name, number) in zip(helpline_cols, helplines):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 2rem;">{icon}</div>
                <div style="color: #f0e6ff; font-weight: 600; margin: 8px 0;">{name}</div>
                <div style="color: #e85a8f; font-size: 1.3rem; font-weight: 700;">{number}</div>
            </div>
            """, unsafe_allow_html=True)

def render_guardian_mode():
    st.markdown('<h1 class="main-title">Guardian Mode</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Real-time location sharing with your trusted contacts</p>', unsafe_allow_html=True)
    
    # Status banner
    if st.session_state.guardian_mode_active:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #2ed573 0%, #26ab5f 100%); 
                    border-radius: 12px; padding: 16px; text-align: center; margin-bottom: 20px;">
            <span class="status-active"></span>
            <span style="color: white; font-weight: 600;">Guardian Mode is ACTIVE - Your guardians are watching</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #3d3555 0%, #2d2640 100%); 
                    border-radius: 12px; padding: 16px; text-align: center; margin-bottom: 20px; border: 1px solid #4d4565;">
            <span style="color: #9d95b8; font-weight: 600;">Guardian Mode is INACTIVE - Enable to start sharing</span>
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:

        # Trip controls
        st.markdown("<br>", unsafe_allow_html=True)
        
        if not st.session_state.trip_active:
            st.markdown("""
            <div class="card">
                <div class="card-header">📍 Start a Trip</div>
            </div>
            """, unsafe_allow_html=True)
            
            with st.form("trip_form"):
                start_loc = st.text_input("Starting Location", placeholder="Current location or enter address")
                dest_loc = st.text_input("Destination", placeholder="Where are you going?")
                travel_mode = st.selectbox("Travel Mode", ["Walking", "Public Transport", "Cab/Taxi", "Personal Vehicle"])
                
                if st.form_submit_button("🚀 Start Trip", use_container_width=True, type="primary"):
                    if start_loc and dest_loc:
                        st.session_state.trip_active = True
                        st.session_state.guardian_mode_active = True
                        st.success("Trip started! Your guardians have been notified.")
                        st.rerun()
                    else:
                        st.error("Please enter both starting and destination locations")
        else:
            trip_col1, trip_col2, trip_col3 = st.columns(3)
            with trip_col1:
                if st.button("✅ I'm Safe", use_container_width=True):
                    st.session_state.check_ins += 1
                    st.success("Check-in recorded!")
            with trip_col2:
                if st.button("📍 Update Location", use_container_width=True):
                    st.info("Location updated!")
            with trip_col3:
                if st.button("🛑 End Trip", use_container_width=True, type="secondary"):
                    st.session_state.trip_active = False
                    st.session_state.guardian_mode_active = False
                    st.info("Trip ended. Guardians notified.")
                    st.rerun()
    
    with col2:
        # Guardian Mode Toggle
        st.markdown("""
        <div class="card">
            <div class="card-header">⚡ Quick Controls</div>
        </div>
        """, unsafe_allow_html=True)
        
        guardian_toggle = st.toggle("Enable Guardian Mode", value=st.session_state.guardian_mode_active)
        if guardian_toggle != st.session_state.guardian_mode_active:
            st.session_state.guardian_mode_active = guardian_toggle
            st.rerun()
        
        check_in_interval = st.selectbox("Check-in Reminder", ["Every 5 min", "Every 10 min", "Every 15 min", "Every 30 min"])
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Guardians list
        st.markdown("""
        <div class="card">
            <div class="card-header">👥 Your Guardians</div>
        </div>
        """, unsafe_allow_html=True)
        
        for guardian in st.session_state.guardians:
            initial = guardian["name"][0].upper()
            st.markdown(f"""
            <div class="guardian-card">
                <div class="guardian-avatar">{initial}</div>
                <div>
                    <div style="color: #f0e6ff; font-weight: 600;">{guardian["name"]}</div>
                    <div style="color: #9d95b8; font-size: 0.85rem;">{guardian["phone"]}</div>
                </div>
                <div style="margin-left: auto;">
                    <span class="status-active"></span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Add guardian form
        with st.expander("➕ Add Guardian"):
            new_name = st.text_input("Guardian Name", key="new_guardian_name")
            new_phone = st.text_input("Phone Number", key="new_guardian_phone")
            if st.button("Add Guardian", use_container_width=True):
                if new_name and new_phone:
                    st.session_state.guardians.append({
                        "name": new_name,
                        "phone": new_phone,
                        "active": True
                    })
                    st.success(f"Added {new_name} as guardian!")
                    st.rerun()
        
        # SOS Button
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚨 EMERGENCY SOS", use_container_width=True, type="primary"):
            st.error("🚨 EMERGENCY ALERT SENT TO ALL GUARDIANS!")
        

def render_trip_analyzer():
    st.markdown('<h1 class="main-title">Trip Safety Analyzer</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Analyze your route before you travel</p>', unsafe_allow_html=True)
    
    try:
        from safest_route import run_safest_route
        run_safest_route()
    except Exception as e:
        st.error(f"Error loading safest route module: {e}")

def render_emergency():
    st.markdown('<h1 class="main-title">Emergency SOS</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">One tap to alert your emergency contacts and authorities</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin: 40px 0;">
        <div style="margin-bottom: 20px; color: #9d95b8;">Tap the button below to send an emergency alert</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚨 ACTIVATE SOS", use_container_width=True, type="primary"):
            st.markdown("""
            <div style="background: linear-gradient(135deg, #ff4757 0%, #ff3344 100%);
                        border-radius: 16px; padding: 30px; text-align: center; margin: 20px 0;
                        animation: pulse 1s infinite;">
                <div style="font-size: 3rem;">🚨</div>
                <div style="color: white; font-size: 1.5rem; font-weight: 700; margin: 10px 0;">EMERGENCY ALERT ACTIVATED</div>
                <div style="color: rgba(255,255,255,0.8);">All contacts notified • Location shared • Authorities alerted</div>
            </div>
            """, unsafe_allow_html=True)
           
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Emergency Helplines
    st.markdown("""
    <div class="card">
        <div class="card-header">📞 Emergency Helplines</div>
    </div>
    """, unsafe_allow_html=True)
    
    helplines = [
        ("🚔", "Police", "100", "24/7 Emergency Response"),
        ("🚑", "Ambulance", "102", "Medical Emergency"),
        ("👩", "Women Helpline", "1091", "24/7 Support for Women"),
        
    ]
    
    cols = st.columns(3)
    for idx, (icon, name, number, desc) in enumerate(helplines):
        with cols[idx % 3]:
            st.markdown(f"""
            <div class="metric-card" style="margin-bottom: 16px;">
                <div style="font-size: 2rem;">{icon}</div>
                <div style="color: #f0e6ff; font-weight: 600; margin: 8px 0;">{name}</div>
                <div style="color: #e85a8f; font-size: 1.5rem; font-weight: 700;">{number}</div>
                <div style="color: #9d95b8; font-size: 0.8rem; margin-top: 4px;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Quick actions
   
    if st.button("📍 Share Location"):
        st.success("Location shared!")

    if st.button("📹 Record Video"):
        st.info("Recording started...")

    if st.button("📱 Call Guardian"):
        st.warning("Calling guardian...")

def render_report_incident():
    st.markdown('<h1 class="main-title">Report Incident</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Help keep the community safe by reporting incidents</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="card">
            <div class="card-header">📝 Incident Details</div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("incident_form"):
            incident_type = st.selectbox("Type of Incident", [
                "Harassment", "Eve Teasing", "Stalking", "Unsafe Area",
                "Poor Lighting", "Suspicious Activity", "Other"
            ])
            
            severity = st.select_slider("Severity Level", options=["Low", "Medium", "High", "Critical"])
            
            location = st.text_input("Location", placeholder="Where did this happen?")
            
            date = st.date_input("Date of Incident")
            time_of_day = st.selectbox("Time of Day", ["Morning", "Afternoon", "Evening", "Night", "Late Night"])
            
            description = st.text_area("Description", placeholder="Describe what happened...", height=150)
            
            # Quick tags
            st.markdown("**Quick Tags:**")
            tag_cols = st.columns(4)
            tags = ["Crowded", "Isolated", "Public Transport", "Street", "Mall", "Office Area", "Residential", "Other"]
            selected_tags = []
            for idx, tag in enumerate(tags):
                with tag_cols[idx % 4]:
                    if st.checkbox(tag, key=f"tag_{tag}"):
                        selected_tags.append(tag)
            
            anonymous = st.checkbox("Report Anonymously")
            
            if st.form_submit_button("📤 Submit Report", use_container_width=True, type="primary"):
                if location and description:
                    st.session_state.incidents.append({
                        "type": incident_type,
                        "severity": severity,
                        "location": location,
                        "date": str(date),
                        "description": description[:100] + "..."
                    })
                    st.success("Thank you for your report. This will help keep others safe!")
                else:
                    st.error("Please fill in the required fields")
    
    with col2:
        st.markdown("""
        <div class="card">
            <div class="card-header">📊 Recent Reports</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.incidents:
            for incident in st.session_state.incidents[-5:]:
                severity_class = f"severity-{incident['severity'].lower()}"
                st.markdown(f"""
                <div class="guardian-card {severity_class}">
                    <div>
                        <div style="color: #f0e6ff; font-weight: 600;">{incident['type']}</div>
                        <div style="color: #9d95b8; font-size: 0.8rem;">{incident['location']}</div>
                        <div style="color: #9d95b8; font-size: 0.75rem;">{incident['date']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No recent reports")
        
        st.markdown("<br>", unsafe_allow_html=True)
        

def render_safety_form():
    st.markdown('<h1 class="main-title">Safety Profile</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Personalize your safety recommendations</p>', unsafe_allow_html=True)
    
    tabs = st.tabs(["Personal Info", "Emergency Preferences"])
    
    with tabs[0]:
        st.markdown("""
        <div class="card">
            <div class="card-header">👤 Personal Information</div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Full Name", placeholder="Your name")
            st.selectbox("Age Group", ["18-24", "25-34", "35-44", "45-54", "55+"])
        with col2:
            st.text_input("Emergency Contact", placeholder="Primary contact number")
            st.text_input("Alternate Contact", placeholder="Secondary contact number")
        
        st.text_input("Home Address", placeholder="Your home address (private)")
        st.text_input("Work/School Address", placeholder="Your regular destination")
    
    
    with tabs[1]:
        st.markdown("""
        <div class="card">
            <div class="card-header">🚨 Emergency Preferences</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.selectbox("Preferred Emergency Service", ["Police (100)", "Women Helpline (1091)", "Family First", "Friends First"])
        st.selectbox("SOS Activation Method", ["Single Tap", "Double Tap", "Long Press", "Shake Phone"])
        
        st.checkbox("Auto-call police in emergency")
        st.checkbox("Auto-record audio in emergency")
        st.checkbox("Auto-share location with guardians")
        st.checkbox("Send periodic check-in reminders")
    
   
def render_support():
    st.markdown('<h1 class="main-title">Support & Care</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">You are not alone. We are here for you.</p>', unsafe_allow_html=True)
    
    tabs = st.tabs(["💬 Chat Support", "🧘 Calm Space", "💪 Empowerment"])
    
    with tabs[0]:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            <div class="card">
                <div class="card-header">💬 Talk to Someone</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.info("Our support team is available 24/7. You can talk about anything - your fears, experiences, or just need someone to listen.")
            
            user_message = st.text_area("Type your message...", height=100, placeholder="Share what's on your mind...")
            
            if st.button("Send Message", type="primary"):
                if user_message:
                    st.success("Message sent. A support volunteer will respond soon.")
                    st.markdown("""
                    <div class="quote-card">
                        Thank you for reaching out. Remember, seeking help is a sign of strength, not weakness. 
                        You deserve to feel safe and supported.
                        <div class="quote-author">- StreeTranam Support Team</div>
                    </div>
                    """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="card">
                <div class="card-header">📞 Helplines</div>
            </div>
            """, unsafe_allow_html=True)
            
            helplines = [
                ("Women Helpline", "1091"),
                ("Mental Health", "1800-599-0019"),
                ("NCW", "7827-170-170"),
            ]
            
            for name, number in helplines:
                st.markdown(f"**{name}:** {number}")
    
    with tabs[1]:
        st.markdown("""
        <div class="card" style="text-align: center;">
            <div class="card-header" style="justify-content: center;">🧘 Breathing Exercise</div>
            <p style="color: #9d95b8;">Follow the circle to calm your breathing</p>
            <div class="breathing-circle">
                Breathe
            </div>
            <p style="color: #9d95b8; font-size: 0.9rem;">Inhale 4 seconds • Hold 4 seconds • Exhale 4 seconds</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="card">
                <div class="card-header">🎵 Calming Sounds</div>
            </div>
            """, unsafe_allow_html=True)
            
            sounds = ["Rain Sounds", "Ocean Waves", "Forest Birds", "Gentle Wind"]
            for sound in sounds:
                if st.button(f"▶ {sound}", key=f"sound_{sound}", use_container_width=True):
                    st.info(f"Playing {sound}...")
        
        with col2:
            st.markdown("""
            <div class="card">
                <div class="card-header">📝 Grounding Exercise</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            **5-4-3-2-1 Technique:**
            - **5** things you can SEE
            - **4** things you can TOUCH
            - **3** things you can HEAR
            - **2** things you can SMELL
            - **1** thing you can TASTE
            """)
    

    with tabs[2]:
        st.markdown("""
        <div class="card">
            <div class="card-header">💪 Survivor Stories</div>
        </div>
        """, unsafe_allow_html=True)
        
        quotes = [
            ("I was scared to speak up, but when I did, I found strength I never knew I had.", "Anonymous Survivor"),
            ("Your story is not over yet. Every day you wake up is a victory.", "Support Volunteer"),
            ("Healing is not linear. Some days are harder than others, and that's okay.", "Recovery Mentor"),
            ("You are braver than you believe, stronger than you seem, and loved more than you know.", "Community Member"),
        ]
        
        for quote, author in quotes:
            st.markdown(f"""
            <div class="quote-card">
                "{quote}"
                <div class="quote-author">- {author}</div>
            </div>
            """, unsafe_allow_html=True)

def render_settings():
    st.markdown('<h1 class="main-title">Settings</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Customize your StreeTranam experience</p>', unsafe_allow_html=True)
    
    tabs = st.tabs(["Account", "Notifications", "Privacy", "About"])
    
    with tabs[0]:
        st.markdown("""
        <div class="card">
            <div class="card-header">👤 Account Settings</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.text_input("Display Name", value="User")
        st.text_input("Email", value="user@example.com")
        st.text_input("Phone Number", value="+91 98765 43210")
        
        if st.button("Update Profile", type="primary"):
            st.success("Profile updated!")
        
        st.markdown("---")
        
       
        if st.button("Delete Account", type="secondary"):
            st.warning("Are you sure? This action cannot be undone.")
    
    with tabs[1]:
        st.markdown("""
        <div class="card">
            <div class="card-header">🔔 Notification Settings</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.toggle("Push Notifications", value=True)
        st.toggle("Check-in Reminders", value=True)
        st.toggle("Safety Alerts", value=True)
        st.toggle("Community Reports", value=False)
        st.toggle("Tips & Resources", value=True)
        
        st.selectbox("Reminder Frequency", ["Every 5 minutes", "Every 10 minutes", "Every 15 minutes", "Every 30 minutes"])
    
    with tabs[2]:
        st.markdown("""
        <div class="card">
            <div class="card-header">🔒 Privacy Settings</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.toggle("Share location with guardians", value=True)
        st.toggle("Anonymous incident reporting", value=True)
        st.toggle("Show profile to community", value=False)
        st.toggle("Allow data for safety research", value=True)
        
        st.markdown("---")
        
        if st.button("Download My Data"):
            st.info("Your data export will be ready shortly.")
        
        if st.button("Clear All Data"):
            st.warning("This will remove all your local data.")
    
    with tabs[3]:
        st.markdown("""
        <div style="text-align: center; padding: 40px;">
            <div style="font-size: 4rem;">🛡️</div>
            <div class="main-title" style="font-size: 2rem;">StreeTranam</div>
            <div class="subtitle">Safety First, Always</div>
            <div style="color: #9d95b8; margin-top: 20px;">Version 1.0.0</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="card">
            StreeTranam is dedicated to making every woman feel safe, wherever she goes. 
            Our mission is to provide tools and support that empower women to travel 
            confidently and connect with their community for mutual safety.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Contact**\nsupport@streetranam.com")
        with col2:
            st.markdown("**Website**\nwww.streetranam.com")
        with col3:
            st.markdown("**Social**\n@streetranam")

def render_map_page():
    st.markdown('<h1 class="main-title">AI Safety Risk Map</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Live safety monitoring zones</p>', unsafe_allow_html=True)

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="streetranam"
        )

        df = pd.read_sql("SELECT * FROM safety_reports", conn)

    except Exception as e:
        st.error(f"MySQL Error: {e}")
        return

    if df.empty:
        st.warning("No safety reports found.")
        return

    df["issue_type"] = df["issue_type"].astype(str).str.lower().str.strip()

    # KMeans clustering
    X = df[["latitude", "longitude"]]

    k = 6
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    df["cluster"] = kmeans.fit_predict(X)

    centers = kmeans.cluster_centers_

    # Risk classification
    high_risk = {"rape", "assault", "stalking", "harassment", "suspicious_activity"}
    medium_risk = {"theft", "chain_snatching", "eve_teasing"}

    def get_risk(issue):
        if issue in high_risk:
            return "HIGH"
        elif issue in medium_risk:
            return "MEDIUM"
        else:
            return "LOW"

    df["risk"] = df["issue_type"].apply(get_risk)

    color_map = {
        "HIGH": "red",
        "MEDIUM": "orange",
        "LOW": "green"
    }

    # Cluster score
    cluster_score = {}

    for i in range(k):
        temp = df[df["cluster"] == i]

        score = (
            (temp["risk"] == "HIGH").sum() * 3 +
            (temp["risk"] == "MEDIUM").sum() * 2 +
            (temp["risk"] == "LOW").sum()
        )

        cluster_score[i] = score

    def get_cluster_color(i):
        score = cluster_score[i]

        if score >= 10:
            return "red"
        elif score >= 5:
            return "orange"
        else:
            return "green"

    # Create map
    m = folium.Map(
        location=[17.3850, 78.4867],
        zoom_start=11
    )

    # Add zones
    for i, center in enumerate(centers):
        folium.Circle(
            location=[center[0], center[1]],
            radius=900,
            color=get_cluster_color(i),
            fill=True,
            fill_opacity=0.12,
            weight=2,
            popup=f"Zone {i}"
        ).add_to(m)

    # Add incident markers
    for _, row in df.iterrows():
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=6,
            color=color_map[row["risk"]],
            fill=True,
            fill_color=color_map[row["risk"]],
            fill_opacity=0.9,
            popup=f"""
            Area: {row['area_name']}<br>
            Issue: {row['issue_type']}<br>
            Risk: {row['risk']}<br>
            Zone: {row['cluster']}
            """
        ).add_to(m)

    # Display map
    st_folium(m, width=1200, height=600)

    st.subheader("📍 Alerts Near You")

    alerts = df[df["risk"] == "HIGH"].head(5)

    if alerts.empty:
        st.success("✅ No high-risk alerts nearby")
    else:
        for _, row in alerts.iterrows():
            st.warning(
                f"📍 {row['area_name']} • {row['issue_type']} • Zone {row['cluster']}"
            )




# Route to the correct page
page_functions = {
    'dashboard': render_dashboard,
    'guardian': render_guardian_mode,
    'trip': render_trip_analyzer,
    'map_page': render_map_page,
    'emergency': render_emergency,
    'report': render_report_incident,
    'safety_form': render_safety_form,
    'support': render_support,
    'settings': render_settings,
}




# Render the current page
if st.session_state.current_page in page_functions:
    page_functions[st.session_state.current_page]()
else:
    render_dashboard()