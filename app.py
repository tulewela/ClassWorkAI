import streamlit as st

# --- 1. SEITEN-KONFIGURATION ---
st.set_page_config(
    page_title="ClassWork AI",
    page_icon="🦉",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. GLOBALER DESIGN-STIL & CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
        color: #333333;
        background-color: #FFFFFF;
    }
    
    .block-container {
        padding-top: 2.5rem;
        padding-bottom: 3rem;
        max-width: 1100px;
    }

    /* Header & Hero */
    .header-container {
        text-align: center;
        margin-bottom: 35px;
    }
    .app-title {
        font-size: 2.6rem;
        font-weight: 700;
        color: #2D3748;
        margin-bottom: 6px;
    }
    .app-subtitle {
        font-size: 1.1rem;
        color: #718096;
        font-weight: 300;
    }

    /* Buttons Styling */
    div.stButton > button {
        width: 100%;
        border-radius: 12px !important;
        height: 60px;
        font-size: 1.05rem !important;
        font-weight: 600 !important;
        border: none !important;
        transition: all 0.2s ease-in-out !important;
        box-shadow: 0 4px 12px rgba(75, 192, 200, 0.15) !important;
    }
    div.stButton > button[kind="primary"] {
        background-color: #4BC0C8 !important;
        color: white !important;
    }
    div.stButton > button[kind="primary"]:hover {
        background-color: #3baab2 !important;
        transform: translateY(-2px);
    }
    div.stButton > button[kind="secondary"] {
        background-color: #E6F7F8 !important;
        color: #2C7A7E !important;
        border: 1.5px solid #4BC0C8 !important;
    }
    div.stButton > button[kind="secondary"]:hover {
        background-color: #d1f1f3 !important;
        transform: translateY(-2px);
    }

    /* Info-Cards (Wie es funktioniert) */
    .feature-card {
        background: #F7FAFC;
        border-radius: 14px;
        padding: 20px 16px;
        text-align: center;
        border: 1px solid #E2E8F0;
        height: 100%;
    }
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 10px;
    }
    .feature-label {
        font-size: 1rem;
        font-weight: 600;
        color: #2D3748;
        margin-bottom: 4px;
    }
    .feature-text {
        font-size: 0.8rem;
        color: #718096;
        line-height: 1.4;
    }

    /* Schüler-Kacheln (Teacher Dashboard) */
    .student-card {
        background-color: #FFFFFF;
        border-radius: 14px;
        padding: 18px;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.04);
        border: 1px solid #E2E8F0;
        margin-bottom: 16px;
        transition: transform 0.2s ease;
    }
    .student-name {
        font-size: 1.15rem;
        font-weight: 700;
        color: #2D3748;
        margin-bottom: 4px;
    }
    .student-app {
        font-size: 0.85rem;
        color: #4A5568;
        margin-bottom: 10px;
        font-weight: 500;
    }
    .status-badge {
        display: inline-block;
        padding: 5px 12px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.8rem;
    }
    .status-focus {
        background-color: rgba(102, 187, 106, 0.15);
        color: #2E7D32;
        border: 1px solid rgba(102, 187, 106, 0.3);
    }
    .status-distracted {
        background-color: rgba(239, 83, 80, 0.15);
        color: #C62828;
        border: 1px solid rgba(239, 83, 80, 0.3);
    }
    .update-time {
        font-size: 0.75rem;
        color: #A0AEC0;
        margin-top: 8px;
    }
    
    /* Raum-Code Banner */
    .room-code-box {
        background-color: #E6F7F8;
        color: #2C7A7E;
        padding: 10px 20px;
        border-radius: 12px;
        font-weight: 700;
        font-size: 1.1rem;
        border: 1px solid #4BC0C8;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. SESSION STATE INITIALISIERUNG ---
if "page" not in st.session_state:
    st.session_state.page = "home"
if "joined_room" not in st.session_state:
    st.session_state.joined_room = False
if "room_pin" not in st.session_state:
    st.session_state.room_pin = "482 915"
if "student_name" not in st.session_state:
    st.session_state.student_name = ""

def navigate_to(page_name):
    st.session_state.page = page_name

# ==========================================
# 1. STARTBILDSCHIRM (HOME)
# ==========================================
if st.session_state.page == "home":
    st.markdown("""
        <div class="header-container">
            <div style="font-size: 3.5rem; margin-bottom: 5px;">
