import streamlit as st
import random
import os

# 1. Seitengestaltung & Fix gegen Scrollen auf Startseite
st.set_page_config(
    page_title="ClassWork AI",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Custom CSS für den perfekten Startbildschirm & normale Unterseiten (Dein Original-Layout)
st.markdown("""
    <style>
    /* Allgemeine Hintergründe & Schrift */
    .stApp {
        background-color: #FFFFFF;
        font-family: 'Poppins', 'Roboto', sans-serif;
        color: #2D3748;
    }
    
    /* Streamlit Standard-Elemente ausblenden */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* ECHTE GROSSE QUADRATISCHE BUTTONS FÜR DEN STARTBILDSCHIRM (HTML-basiert) */
    .home-btn-container {
        display: flex;
        justify-content: center;
        gap: 30px;
        margin-top: 30px;
    }
    
    .home-custom-btn {
        background-color: #7AC4C3 !important;
        color: #FFFFFF !important;
        border-radius: 28px !important;
        width: 320px !important;
        height: 280px !important;
        font-size: 28px !important;
        font-weight: 800 !important;
        border: 4px solid #3B9392 !important;
        box-shadow: 0 15px 35px rgba(122, 196, 195, 0.4) !important;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        text-decoration: none !important;
        transition: all 0.2s ease-in-out;
        line-height: 1.4;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    .home-custom-btn:hover {
        background-color: #65B3B2 !important;
        border-color: #287271 !important;
        transform: translateY(-3px);
        color: #FFFFFF !important;
    }
    
    /* Normale Buttons auf den Unterseiten */
    div.stButton > button {
        border-radius: 14px;
        font-weight: 600;
    }
    
    /* Eingabefelder weich abgerundet */
    .stTextInput input {
        border-radius: 16px !important;
        border: 2px solid #CBD5E0 !important;
        padding: 16px !important;
        font-size: 16px !important;
        background-color: #FAFCFF !important;
    }

    /* Raum-Badge */
    .room-badge {
        background-color: #7AC4C3;
        color: white;
        padding: 10px 22px;
        border-radius: 25px;
        font-weight: bold;
        font-size: 18px;
        box-shadow: 0 4px 15px rgba(122, 196, 195, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# Hilfsfunktion zum sicheren Laden deines PNG-Logos
def render_logo(width=80):
    if os.path.exists("ClassWorkAILogo.png"):
        st.image("ClassWorkAILogo.png", width=width)
    else:
        st.markdown(f"<h3 style='margin:0;'>Logo fehlt (ClassWorkAILogo.png hochladen)</h3>", unsafe_allow_html=True)

# Session State Initialisierung
if "page" not in st.session_state:
    st.session_state.page = "home"

if "room_code" not in st.session_state:
    st.session_state.room_code = None

if "connected_students" not in st.session_state:
    st.session_state.connected_students = []

if "confirm_close" not in st.session_state:
    st.session_state.confirm_close = False

if "selected_student" not in st.session_state:
    st.session_state.selected_student = "Anna S."

# Query Parameters am Anfang abfangen
query_params = st.query_params
if "nav" in query_params:
    st.session_state.page = query_params["nav"]

if "action" in query_params and query_params["action"] == "host":
    if not st.session_state.room_code:
        st.session_state.room_code = str(random.randint(100000, 999999))
        st.session_state.connected_students = []
    st.session_state.confirm_close = False
    st.session_state.page = "teacher_dashboard"
    if "action" in st.query_params:
        del st.query_params["action"]
    st.query_params["nav"] = "teacher_dashboard"

def navigate_to(page_name):
    st.session_state.page = page_name
    st.query_params["nav"] = page_name
    st.rerun()


# ==========================================
# 1. STARTBILDSCHIRM (HOME)
# ==========================================
if st.session_state.page == "home":
    top_left_col, _ = st.columns([1, 11])
    with top_left_col:
        render_logo(width=90)

    st.markdown("<h1 style='text-align: center; color: #1A202C; font-weight: 800; font-size: 46px; margin-top: -40px; margin-bottom: 5px;'>ClassWork AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #4A5568; font-size: 18px; margin-bottom: 30px;'>Datenschutzfreundliche Aktivitätsmeldung für konzentriertes Lernen.</p>", unsafe_allow_html=True)

    st.markdown("""
        <div class="home-btn-container">
            <a href="?nav=teacher_dashboard&action=host" target="_self" class="home-custom-btn">Als Lehrer<br>Raum hosten</a>
            <a href="?nav=student_join" target="_self" class="home-custom-btn">Als Schüler<br>Raum beitreten</a>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 35px;'></div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #A0AEC0; font-size: 13px;'>KI-Analyse im Hintergrund, ohne Video</p>", unsafe_allow_html=True)


# ==========================================
# 2. SCHÜLER-ANSICHT (RAUM BEITRETEN)
# ==========================================
elif st.session_state.page == "student_join":
    col_t1, col_t2, col_t3 = st.columns([1, 8, 2])
    with col_t1:
        render_logo(width=50)
    with col_t2:
        st.markdown("<h2 style='margin:0; font-size: 22px; line-height: 50px;'>ClassWork AI: Schüler-Ansicht</h2>", unsafe_allow_html=True)
    with col_t3:
        if st.button("🏠 Home", key="home_btn_1"):
            navigate_to("home")
            
    st.markdown("---")
    
    _, form_col, _ = st.columns([1, 1.3, 1])
    with form_col:
        st.markdown("<br>", unsafe_allow_html=True)
        
        with st.container(border=True):
            st.markdown("### Raum beitreten")
            entered_code = st.text_input("Raum-Code", placeholder="Gib den 6-stelligen Raum-Code ein", max_chars=6, label_visibility="collapsed")
            student_name = st.text_input("Dein Name", placeholder="Dein Vorname (z.B. Alex)")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Raum beitreten", key="submit_join"):
                current_room = str(st.session_state.room_code).strip() if st.session_state.room_code else ""
                user_code = entered_code.strip()
                clean_name = student_name.strip()
                
                if current_room and user_code == current_room:
                    if clean_name and clean_name not in st.session_state.connected_students:
                        st.session_state.connected_students.append(clean_name)
                        st.success(f"Erfolgreich mit Raum {user_code} verbunden!")
                    elif not clean_name:
                        st.warning("Bitte gib deinen Namen ein.")
                    else:
                        st.info("Du bist bereits mit diesem Raum verbunden.")
                elif not current_room:
                    st.error("Es ist aktuell kein Raum aktiv. Der Lehrer muss zuerst einen Raum hosten.")
                else:
                    st.error("Falscher Raum-Code. Bitte überprüfe den Code.")
                    
        st.markdown("<br>", unsafe_allow_html=True)
        st.info("🔒 **Deine Privatsphäre ist geschützt.** Der Lehrer sieht keine Bildschirminhalte.")


# ==========================================
# 3. LEHRER-DASHBOARD (KLASSENÜBERSICHT)
# ==========================================
elif st.session_state.page == "teacher_dashboard":
    if not st.session_state.room_code:
        st.session_state.room_code = str(random.randint(100000, 999999))

    col_t1, col_t2, col_t3, col_t4, col_t5 = st.columns([0.8, 3.8, 2, 1.8, 1.6])
    with col_t1:
        render_logo(width=50)
    with col_t2:
        st.markdown("<h2 style='margin:0; font-size: 22px; line-height: 50px;'>ClassWork AI: Lehrer-Dashboard</h2>", unsafe_allow_html=True)
    with col_t3:
        if st.button("⚙️ Einstellungen", key="settings_btn"):
            navigate_to("teacher_settings")
    with col_t4:
        display_code = st.session_state.room_code
        st.markdown(f"<div style='text-align: right;'><span class='room-badge'>Raum: {display_code}</span></div>", unsafe_allow_html=True)
    with col_t5:
        if st.button("Raum schließen", key="close_room_btn"):
            st.session_state.confirm_close = True
            st.rerun()
            
    st.markdown("---")
    
    # Sicherheitsabfrage für Raum schließen
    if st.session_state.confirm_close:
        with st.container(border=True):
            st.warning("⚠️ **Möchtest du den Raum wirklich schließen?** Alle verbundenen Schüler werden getrennt.")
            c_ja, c_nein, _ = st.columns([1, 1, 3])
            with c_ja:
                if st.button("Ja", key="yes_close"):
                    st.session_state.room_code = None
                    st.session_state.connected_students = []
                    st.session_state.confirm_close = False
                    navigate_to("home")
            with c_nein:
                if st.button("Nein", key="no_close"):
                    st.session_state.confirm_close = False
                    st.rerun()
        st.markdown("<br>", unsafe_allow_html=True)

    if not st.session_state.connected_students:
        st.info(f"Der Raum `{display_code}` ist aktuell noch leer. Teile den 6-stelligen Code mit deinen Schülerinnen und Schülern, damit sie beitreten können.")
    else:
        st.subheader(f"Verbundene Schüler ({len(st.session_state.connected_students)})")
        students = [{"name": name, "status": "green", "time": "Gerade eben"} for name in st.session_state.connected_students]
        
        row1_cols = st.columns(3)
        row2_cols = st.columns(3)
        all_cols = row1_cols + row2_cols
        
        for i, student in enumerate(students):
            if i < len(all_cols):
                with all_cols[i]:
                    with st.container(border=True):
                        c1, c2 = st.columns([4, 1])
                        with c1:
                            st.markdown(f"**{student['name']}**")
                        with c2:
                            st.markdown(f"<div style='text-align: right;'>🟢</div>", unsafe_allow_html=True)
                        
                        st.markdown("<div style='text-align: center; padding: 15px 0;'><span style='font-size: 36px;'>👤</span></div>", unsafe_allow_html=True)
                        
                        bc1, bc2 = st.columns([2, 2])
                        with bc1:
                            st.caption(student["time"])
                        with bc2:
                            if st.button("Details", key=f"btn_{i}"):
                                st.session_state.selected_student = student["name"]
                                navigate_to("student_detail")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center; background: #F8FAFC; padding: 12px; border-radius: 14px; font-weight: 500;'>🟢 Unterrichtsrelevant &nbsp;|&nbsp; 🔴 Ablenkung &nbsp;|&nbsp; 🟡 Unsicher</div>", unsafe_allow_html=True)


# ==========================================
# 4. SCHÜLER-DETAILANSICHT (HISTORIE)
