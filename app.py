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

# 2. Dejates exaktes Layout-CSS (Startbildschirm-Buttons groß, quadratisch, #7AC4C3, Rest normal)
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
    
    /* RIESIGE, GLEICHGROSSE, QUADRATISCHE STARTSEITEN-BUTTONS (#7AC4C3) */
    .home-buttons div.stButton > button {
        background-color: #7AC4C3 !important;
        color: #FFFFFF !important;
        border-radius: 28px !important;
        height: 280px !important;
        font-size: 28px !important;
        font-weight: 800 !important;
        border: 4px solid #3B9392 !important;
        box-shadow: 0 15px 35px rgba(122, 196, 195, 0.4) !important;
        transition: all 0.2s ease-in-out;
        width: 100%;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        line-height: 1.3;
    }
    
    .home-buttons div.stButton > button:hover {
        background-color: #65B3B2 !important;
        border-color: #287271 !important;
        transform: translateY(-2px);
    }
    
    /* Alle anderen Buttons auf den Unterseiten (normal groß) */
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

# Hilfsfunktion zum sicheren Laden des Logos
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

if "confirm_close_room" not in st.session_state:
    st.session_state.confirm_close_room = False

def navigate_to(page_name):
    st.session_state.page = page_name


# ==========================================
# 1. STARTBILDSCHIRM (HOME) - Exakt nach Wunschlayout
# ==========================================
if st.session_state.page == "home":
    top_left_col, _ = st.columns([1, 11])
    with top_left_col:
        render_logo(width=90)

    st.markdown("<h1 style='text-align: center; color: #1A202C; font-weight: 800; font-size: 46px; margin-top: -30px; margin-bottom: 5px;'>ClassWork AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #4A5568; font-size: 18px; margin-bottom: 25px;'>Datenschutzfreundliche Aktivitätsmeldung für konzentriertes Lernen.</p>", unsafe_allow_html=True)

    st.markdown('<div class="home-buttons">', unsafe_allow_html=True)
    _, btn_container, _ = st.columns([0.2, 9.6, 0.2])
    with btn_container:
        btn_col1, btn_col2 = st.columns(2)
        
        with btn_col1:
            if st.button("Als Lehrer\nRaum hosten", key="host_btn"):
                if not st.session_state.room_code:
                    st.session_state.room_code = str(random.randint(100000, 999999))
                    st.session_state.connected_students = []
                st.session_state.confirm_close_room = False
                navigate_to("teacher_dashboard")
                st.rerun()
                
        with btn_col2:
            if st.button("Als Schüler\nRaum beitreten", key="join_btn"):
                navigate_to("student_join")
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
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
            st.rerun()
            
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
                if st.session_state.room_code and entered_code == st.session_state.room_code:
                    if student_name and student_name not in st.session_state.connected_students:
                        st.session_state.connected_students.append(student_name)
                        st.success(f"Erfolgreich mit Raum {entered_code} verbunden!")
                    elif not student_name:
                        st.warning("Bitte gib deinen Namen ein.")
                    else:
                        st.info("Du bist bereits mit diesem Raum verbunden.")
                elif entered_code != st.session_state.room_code:
                    st.error("Falscher Raum-Code oder kein Raum aktiv.")
                else:
                    st.warning("Bitte gib den 6-stelligen Raum-Code ein.")
                    
        st.markdown("<br>", unsafe_allow_html=True)
        st.info("🔒 **Deine Privatsphäre ist geschützt.** Der Lehrer sieht keine Bildschirminhalte.")


# ==========================================
# 3. LEHRER-DASHBOARD (KLASSENÜBERSICHT)
# ==========================================
elif st.session_state.page == "teacher_dashboard":
    col_t1, col_t2, col_t3, col_t4, col_t5 = st.columns([0.8, 3.8, 2, 1.8, 1.6])
    with col_t1:
        render_logo(width=50)
    with col_t2:
        st.markdown("<h2 style='margin:0; font-size: 22px; line-height: 50px;'>ClassWork AI: Lehrer-Dashboard</h2>", unsafe_allow_html=True)
    with col_t3:
        if st.button("⚙️ Einstellungen", key="settings_btn"):
            navigate_to("teacher_settings")
            st.rerun()
    with col_t4:
        display_code = st.session_state.room_code if st.session_state.room_code else "------"
        st.markdown(f"<div style='text-align: right;'><span class='room-badge'>Raum: {display_code}</span></div>", unsafe_allow_html=True)
    with col_t5:
        if st.button("Raum schließen", key="close_room_init"):
            st.session_state.confirm_close_room = True
            st.rerun()
            
    st.markdown("---")
    
    # Sicherheitsabfrage für Raum schließen
    if st.session_state.confirm_close_room:
        with st.container(border=True):
            st.warning("⚠️ **Raum wirklich schließen?** Alle verbundenen Schüler werden getrennt.")
            col_ja, col_nein, _ = st.columns([1, 1, 3])
            with col_ja:
                if st.button("Ja", key="close_yes"):
                    st.session_state.room_code = None
                    st.session_state.connected_students = []
                    st.session_state.confirm_close_room = False
                    navigate_to("home")
                    st.rerun()
            with col_nein:
                if st.button("Nein", key="close_no"):
                    st.session_state.confirm_close_room = False
                    st.rerun()
        st.markdown("<br>", unsafe_allow_html=True)

    if not st.session_state.room_code:
        st.info("Es ist aktuell kein Raum aktiv. Kehre zum Startbildschirm zurück und hoste einen neuen Raum.")
    elif not st.session_state.connected_students:
        st.info(f"Der Raum `{display_code}` ist aktuell noch leer. Teile den 6-stelligen Code mit deinen Schülerinnen und Schülern, damit sie beitreten können.")
    else:
        st.subheader(f"Verbundene Schüler ({len(st.session_state.connected_students)})")
        cols = st.columns(3)
        for i, name in enumerate(st.session_state.connected_students):
            with cols[i % 3]:
                with st.container(border=True):
                    c1, c2 = st.columns([4, 1])
                    with c1:
                        st.markdown(f"**{name}**")
                    with c2:
                        st.markdown("<div style='text-align: right;'>🟢</div>", unsafe_allow_html=True)
                    
                    st.markdown("<div style='text-align: center; padding: 15px 0;'><span style='font-size: 36px;'>👤</span></div>", unsafe_allow_html=True)
                    st.caption("Status: Verbunden")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center; background: #F8FAFC; padding: 12px; border-radius: 14px; font-weight: 500;'>🟢 Unterrichtsrelevant &nbsp;|&nbsp; 🔴 Ablenkung &nbsp;|&nbsp; 🟡 Unsicher</div>", unsafe_allow_html=True)


# ==========================================
# 4. LEHRER-EINSTELLUNGEN
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
        if st.button("Raum zurücksetzen / Schließen"):
            st.session_state.room_code = None
            st.session_state.connected_students = []
            st.success("Der Raum wurde geschlossen.")
            
    with st.container(border=True):
        st.markdown("#### 🔒 Datenschutz Regelungen")
        st.write("Umfassende Datenschutz-Garantie: Lokale Analyse, keine Bildschirminhalte.")
        st.success("DSGVO Audit: Bestätigt 🟢")
            
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚪 Logout / Abmelden", key="logout_btn"):
        navigate_to("home")
        st.rerun()
