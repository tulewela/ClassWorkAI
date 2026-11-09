import streamlit as st
from PIL import Image
import os

# 1. Seitengestaltung
st.set_page_config(
    page_title="ClassWork AI",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Aggressives Custom CSS für das echte EdTech-Design, riesige Buttons & Petrol-Farben
st.markdown("""
    <style>
    /* Allgemeine Hintergründe & Schrift */
    .stApp {
        background-color: #FFFFFF;
        font-family: 'Poppins', 'Roboto', sans-serif;
        color: #2D3748;
    }
    
    /* Streamlit Standard-Elemente für sauberes Layout ausblenden */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* RIESIGE, SCHÖNE HAUPT-BUTTONS (Petrol & modern) */
    .stButton > button {
        background-color: #4BC0C8 !important;
        color: white !important;
        border-radius: 16px !important;
        padding: 18px 24px !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        border: none !important;
        box-shadow: 0 6px 20px rgba(75, 192, 200, 0.4) !important;
        transition: all 0.2s ease-in-out;
        width: 100%;
    }
    
    .stButton > button:hover {
        background-color: #3aaab2 !important;
        box-shadow: 0 8px 25px rgba(75, 192, 200, 0.6) !important;
        transform: translateY(-2px);
    }

    /* Sekundäre / Zurück-Buttons etwas dezenter, aber auch schön abgerundet */
    button[kind="secondary"] {
        background-color: #F0F4F8 !important;
        color: #2D3748 !important;
        border: 2px solid #CBD5E0 !important;
        box-shadow: none !important;
    }
    
    /* Eingabefelder extrem weich abgerundet */
    .stTextInput input {
        border-radius: 16px !important;
        border: 2px solid #CBD5E0 !important;
        padding: 16px !important;
        font-size: 16px !important;
        background-color: #FAFCFF !important;
    }

    /* Top-Bar im einheitlichen Look */
    .top-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 15px 25px;
        background: #F8FAFC;
        border-radius: 16px;
        margin-bottom: 30px;
        border: 1px solid #EDF2F7;
    }
    
    /* Raum-Badge */
    .room-badge {
        background-color: #4BC0C8;
        color: white;
        padding: 10px 22px;
        border-radius: 25px;
        font-weight: bold;
        font-size: 18px;
        box-shadow: 0 4px 15px rgba(75, 192, 200, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# Hilfsfunktion zum sicheren Laden deines Logos
def render_logo(width=80):
    if os.path.exists("ClassWorkAILogo.png"):
        st.image("ClassWorkAILogo.png", width=width)
    else:
        st.markdown(f"<h3 style='margin:0;'>🦉</h3>", unsafe_allow_html=True)

# Navigation via Session State
if "page" not in st.session_state:
    st.session_state.page = "home"

if "selected_student" not in st.session_state:
    st.session_state.selected_student = "Anna S."

def navigate_to(page_name):
    st.session_state.page = page_name


# ==========================================
# 1. STARTBILDSCHIRM (HOME)
# ==========================================
if st.session_state.page == "home":
    _, center_col, _ = st.columns([1, 2.2, 1])
    
    with center_col:
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Logo zentriert (Groß und sauber)
        cols_logo = st.columns([1, 1.2, 1])
        with cols_logo[1]:
            render_logo(width=130)
            
        st.markdown("<h1 style='text-align: center; color: #1A202C; font-weight: 800; font-size: 38px; margin-top: 10px;'>ClassWork AI</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #4A5568; font-size: 18px; margin-bottom: 40px;'>Datenschutzfreundliche Aktivitätsmeldung für konzentriertes Lernen.</p>", unsafe_allow_html=True)

        # Große, präzise Haupt-Buttons nebeneinander
        btn_col1, btn_col2 = st.columns(2)
        
        with btn_col1:
            if st.button("🏫 Als Lehrer Raum hosten"):
                navigate_to("teacher_dashboard")
                st.rerun()
                
        with btn_col2:
            if st.button("💻 Als Schüler Raum beitreten"):
                navigate_to("student_join")
                st.rerun()

        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #A0AEC0; font-size: 14px;'>KI-Analyse im Hintergrund, ohne Video</p>", unsafe_allow_html=True)


# ==========================================
# 2. SCHÜLER-ANSICHT (RAUM BEITRETEN)
# ==========================================
elif st.session_state.page == "student_join":
    # Einheitliche Top-Leiste mit Logo statt Eulen-Emoji
    col_t1, col_t2, col_t3 = st.columns([1, 8, 2])
    with col_t1:
        render_logo(width=50)
    with col_t2:
        st.markdown("<h2 style='margin:0; font-size: 22px; line-height: 50px;'>ClassWork AI: Schüler-Ansicht</h2>", unsafe_allow_html=True)
    with col_t3:
        if st.button("🏠 Home", key="home_btn_1"):
            navigate_to("home")
            st.rerun()
            
    st.markdown("---")
    
    _, form_col, _ = st.columns([1, 1.3, 1])
    with form_col:
        st.markdown("<br>", unsafe_allow_html=True)
        
        with st.container(border=True):
            st.markdown("### Raum beitreten")
            room_code_input = st.text_input("Raum-Code", placeholder="Gib den 6-stelligen Raum-Code ein", label_visibility="collapsed")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("💻 Raum beitreten"):
                if room_code_input == "482915" or len(room_code_input) == 6:
                    st.success("Erfolgreich verbunden!")
                else:
                    st.warning("Bitte gib einen gültigen 6-stelligen Code ein (z.B. 482915)")
                    
        st.markdown("<br>", unsafe_allow_html=True)
        st.info("🔒 **Deine Privatsphäre ist geschützt.** Der Lehrer sieht keine Bildschirminhalte.")


# ==========================================
# 3. LEHRER-DASHBOARD (KLASSENÜBERSICHT)
# ==========================================
elif st.session_state.page == "teacher_dashboard":
    # Top-Leiste mit Logo & Raum-Badge
    col_t1, col_t2, col_t3, col_t4 = st.columns([0.8, 5.2, 2, 2])
    with col_t1:
        render_logo(width=50)
    with col_t2:
        st.markdown("<h2 style='margin:0; font-size: 22px; line-height: 50px;'>ClassWork AI: Lehrer-Dashboard</h2>", unsafe_allow_html=True)
    with col_t3:
        if st.button("⚙️ Einstellungen", key="settings_btn"):
            navigate_to("teacher_settings")
            st.rerun()
    with col_t4:
        st.markdown("<div style='text-align: right;'><span class='room-badge'>Raum: 482 915</span></div>", unsafe_allow_html=True)
        
    st.markdown("---")
    
    students = [
        {"name": "Max", "status": "green", "time": "Vor 2 Sek."},
        {"name": "Anna S.", "status": "red", "time": "Vor 5 Sek."},
        {"name": "Lukas", "status": "yellow", "time": "Vor 3 Sek."},
        {"name": "Ben", "status": "green", "time": "Vor 1 Sek."},
        {"name": "Sophie", "status": "red", "time": "Vor 4 Sek."},
        {"name": "Mia", "status": "yellow", "time": "Vor 6 Sek."}
    ]
    
    row1_cols = st.columns(3)
    row2_cols = st.columns(3)
    all_cols = row1_cols + row2_cols
    
    for i, student in enumerate(students):
        with all_cols[i]:
            if student["status"] == "green":
                dot = "🟢"
            elif student["status"] == "red":
                dot = "🔴"
            else:
                dot = "🟡"
                
            with st.container(border=True):
                c1, c2 = st.columns([4, 1])
                with c1:
                    st.markdown(f"**{student['name']}**")
                with c2:
                    st.markdown(f"<div style='text-align: right;'>{dot}</div>", unsafe_allow_html=True)
                
                st.markdown("<div style='text-align: center; padding: 15px 0;'><span style='font-size: 36px;'>👤</span></div>", unsafe_allow_html=True)
                
                bc1, bc2 = st.columns([2, 2])
                with bc1:
                    st.caption(student["time"])
                with bc2:
                    if student["name"] == "Anna S.":
                        if st.button("Details", key=f"btn_{i}"):
                            st.session_state.selected_student = "Anna S."
                            navigate_to("student_detail")
                            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center; background: #F8FAFC; padding: 12px; border-radius: 14px; font-weight: 500;'>🟢 Unterrichtsrelevant &nbsp;|&nbsp; 🔴 Ablenkung &nbsp;|&nbsp; 🟡 Unsicher</div>", unsafe_allow_html=True)


# ==========================================
# 4. SCHÜLER-DETAILANSICHT (HISTORIE)
# ==========================================
elif st.session_state.page == "student_detail":
    col_t1, col_t2, col_t3 = st.columns([6, 2, 2])
    with col_t1:
        if st.button("⬅️ Zurück zum Dashboard", key="back_dash"):
            navigate_to("teacher_dashboard")
            st.rerun()
    with col_t2:
        st.empty()
    with col_t3:
        st.markdown("<div style='text-align: right;'><span class='room-badge'>Raum: 482 915</span></div>", unsafe_allow_html=True)
        
    st.markdown(f"### {st.session_state.selected_student} - Historie (Detaillierte Liste)")
    st.markdown("---")
    
    history_data = [
        ("09:42:30", "green", "Unterrichtsrelevant", "Dauer: 4 Min. 15 Sek. (Anhaltend)"),
        ("09:38:15", "red", "Ablenkung", "Dauer: 3 Min. 20 Sek."),
        ("09:30:00", "red", "Ablenkung", "Dauer: 3 Min. 0 Sek."),
        ("09:25:40", "red", "Ablenkung", "Dauer: 5 Min. 0 Sek."),
        ("09:20:00", "red", "Ablenkung", "Dauer: 5 Min. 0 Sek."),
        ("09:15:30", "yellow", "Unsicher", "Dauer: 4 Min. 30 Sek."),
        ("09:10:00", "yellow", "Unsicher", "Dauer: 5 Min. 0 Sek."),
        ("09:05:00", "red", "Ablenkung", "Dauer: 4 Min. 30 Sek."),
        ("09:00:00", "yellow", "Unsicher", "Dauer: 4 Min. 30 Sek.")
    ]
    
    for time_stamp, status_color, status_text, duration in history_data:
        dot = "🟢" if status_color == "green" else ("🔴" if status_color == "red" else "🟡")
        
        with st.container(border=True):
            col_h1, col_h2 = st.columns([1, 6])
            with col_h1:
                st.markdown(f"**{time_stamp}**")
            with col_h2:
                st.markdown(f"{dot} **{status_text}**")
                st.caption(duration)
                
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center; background: #F8FAFC; padding: 12px; border-radius: 14px; font-weight: 500;'>🟢 Unterrichtsrelevant &nbsp;|&nbsp; 🔴 Ablenkung &nbsp;|&nbsp; 🟡 Unsicher</div>", unsafe_allow_html=True)


# ==========================================
# 5. LEHRER-EINSTELLUNGEN
# ==========================================
elif st.session_state.page == "teacher_settings":
    col_t1, col_t2 = st.columns([8, 2])
    with col_t1:
        if st.button("⬅️ Zurück zum Dashboard", key="back_dash_2"):
            navigate_to("teacher_dashboard")
            st.rerun()
    with col_t2:
        if st.button("🏠 Home", key="home_btn_2"):
            navigate_to("home")
            st.rerun()
            
    st.markdown("### ⚙️ ClassWork AI: Einstellungen")
    st.markdown("---")
    
    with st.container(border=True):
        st.markdown("#### 👤 Profil & Account")
        st.write("Eingeloggt als: **Lehrer Max M.** (Schule Musterstadt)")
        if st.button("Profil bearbeiten", key="edit_profile"):
            st.toast("Profil-Bearbeitung geöffnet.")
            
    with st.container(border=True):
        st.markdown("#### 🛠️ Systemeinstellungen")
        st.write("**Meldungs-Typen (🟢🔴🟡):** Aktiv")
        st.write("**Benachrichtigungen:** Push-Hinweise bei starker Ablenkung")
        st.markdown("---")
        st.markdown("**Geräte-Verwaltung:**")
        st.checkbox("Schülermodus automatisch erzwingen", value=True)
        st.checkbox("Strenger Datenschutz-Check aktiv", value=True)
        
    with st.container(border=True):
        st.markdown("#### 🔒 Datenschutz Regelungen")
        st.write("Umfassende Datenschutz-Garantie: Lokale Analyse, keine Bildschirminhalte.")
        st.success("DSGVO Audit: Bestätigt 🟢")
        if st.button("Umfassende Regelungen ansehen", key="privacy_btn"):
            st.info("Das System verarbeitet keinerlei Videostreams oder persönliche Inhalte extern.")
            
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🚪 Logout / Abmelden"):
        navigate_to("home")
        st.rerun()
        
    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #A0AEC0; font-size: 12px;'>ClassWork AI v1.0 | DSGVO Audit Status: Erfolgreich</p>", unsafe_allow_html=True)
