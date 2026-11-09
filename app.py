import streamlit as st

# 1. Seitengestaltung (Muss ganz am Anfang stehen)
st.set_page_config(
    page_title="ClassWork AI",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Globales Custom CSS für das exakte Layout, abgerundete Ecken & Farben
st.markdown("""
    <style>
    /* Hintergrund und Schriftart */
    .stApp {
        background-color: #FFFFFF;
        font-family: 'Poppins', 'Roboto', sans-serif;
        color: #333333;
    }
    
    /* Globale Buttons anpassen */
    .stButton > button {
        border-radius: 14px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    /* Eingabefelder abrunden */
    .stTextInput input {
        border-radius: 14px !important;
        border: 2px solid #E2E8F0 !important;
        padding: 12px !important;
    }

    /* Karten / Container Styling (Neumorphismus-Light) */
    .custom-card {
        background: #FFFFFF;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
        border: 1px solid #F0F4F8;
        margin-bottom: 20px;
    }

    /* Top Bar Styling */
    .top-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 20px;
        border-bottom: 1px solid #EFEFEF;
        margin-bottom: 30px;
    }
    
    .room-badge {
        background-color: #4BC0C8;
        color: white;
        padding: 8px 18px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 16px;
        box-shadow: 0 4px 10px rgba(75, 192, 200, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

# Navigation über Session State initialisieren
if "page" not in st.session_state:
    st.session_state.page = "home"

if "selected_student" not in st.session_state:
    st.session_state.selected_student = "Anna S."

def navigate_to(page_name):
    st.session_state.page = page_name


# ==========================================
# 1. ANSICHT: STARTBILDSCHIRM (HOME)
# ==========================================
if st.session_state.page == "home":
    # Zentriertes Layout für den Startbildschirm
    _, center_col, _ = st.columns([1, 2, 1])
    
    with center_col:
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Logo zentriert (Hier wird das hochgeladene Logo "ClassWorkAILogo.jpeg" verwendet)
        try:
            st.image("ClassWorkAILogo.jpeg", width=120)
        except:
            st.markdown("<h1 style='text-align: center;'>🦉</h1>", unsafe_allow_html=True)
            
        st.markdown("<h1 style='text-align: center; color: #1A202C; font-weight: 700; margin-top: 10px;'>ClassWork AI</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #718096; font-size: 16px; margin-bottom: 40px;'>Datenschutzfreundliche Aktivitätsmeldung für konzentriertes Lernen.</p>", unsafe_allow_html=True)

        # Zwei große Haupt-Buttons nebeneinander
        btn_col1, btn_col2 = st.columns(2)
        
        with btn_col1:
            if st.button("🏫 Als Lehrer Raum hosten", use_container_width=True, type="primary"):
                navigate_to("teacher_dashboard")
                st.rerun()
                
        with btn_col2:
            if st.button("💻 Als Schüler Raum beitreten", use_container_width=True):
                navigate_to("student_join")
                st.rerun()

        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #A0AEC0; font-size: 13px;'>KI-Analyse im Hintergrund, ohne Video</p>", unsafe_allow_html=True)


# ==========================================
# 2. ANSICHT: SCHÜLER-ANSICHT (RAUM BEITRETEN)
# ==========================================
elif st.session_state.page == "student_join":
    # Top-Leiste
    col_t1, col_t2 = st.columns([8, 2])
    with col_t1:
        st.markdown("### 🦉 ClassWork AI: Schüler-Ansicht")
    with col_t2:
        if st.button("🏠 Home"):
            navigate_to("home")
            st.rerun()
            
    st.markdown("---")
    
    _, form_col, _ = st.columns([1, 1.2, 1])
    with form_col:
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Zentrierter weißer Container (Card-Look)
        with st.container():
            st.markdown("### Raum beitreten")
            room_code_input = st.text_input("Raum-Code", placeholder="Gib den 6-stelligen Raum-Code ein", label_visibility="collapsed")
            
            if st.button("💻 Raum beitreten", use_container_width=True, type="primary"):
                if room_code_input == "482915" or len(room_code_input) == 6:
                    st.success("Erfolgreich verbunden!")
                else:
                    st.warning("Bitte gib einen gültigen 6-stelligen Code ein (z.B. 482915)")
                    
        st.markdown("<br><br>", unsafe_allow_html=True)
        # Datenschutz-Hinweis Box
        st.info("🔒 **Deine Privatsphäre ist geschützt.** Der Lehrer sieht keine Bildschirminhalte.")


# ==========================================
# 3. ANSICHT: LEHRER-DASHBOARD (KLASSENÜBERSICHT)
# ==========================================
elif st.session_state.page == "teacher_dashboard":
    # Top-Leiste mit Titel und Raum-Badge
    col_t1, col_t2, col_t3 = st.columns([6, 2, 2])
    with col_t1:
        st.markdown("### 🦉 ClassWork AI: Lehrer-Dashboard")
    with col_t2:
        if st.button("⚙️ Einstellungen"):
            navigate_to("teacher_settings")
            st.rerun()
    with col_t3:
        st.markdown("<div style='text-align: right;'><span class='room-badge'>Raum: 482 915</span></div>", unsafe_allow_html=True)
        
    st.markdown("---")
    
    # Grid-Layout für Schüler-Kacheln (2 Reihen à 3 Spalten)
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
            # Status-Punkt Icon festlegen
            if student["status"] == "green":
                dot = "🟢"
            elif student["status"] == "red":
                dot = "🔴"
            else:
                dot = "🟡"
                
            # Kachel-Inhalt als interaktive Karte mit Klick-Funktion auf Anna
            with st.container(border=True):
                c1, c2 = st.columns([4, 1])
                with c1:
                    st.markdown(f"**{student['name']}**")
                with c2:
                    st.markdown(f"<div style='text-align: right;'>{dot}</div>", unsafe_allow_html=True)
                
                st.markdown("<div style='text-align: center; padding: 10px 0;'><span style='font-size: 32px;'>👤</span></div>", unsafe_allow_html=True)
                
                bc1, bc2 = st.columns([2, 2])
                with bc1:
                    st.caption(student["time"])
                with bc2:
                    # Wenn man auf Anna klickt, öffnet sich ihre Detailansicht
                    if student["name"] == "Anna S.":
                        if st.button("Details", key=f"btn_{i}", use_container_width=True):
                            st.session_state.selected_student = "Anna S."
                            navigate_to("student_detail")
                            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    # Legende unten
    st.markdown("<div style='text-align: center; background: #F8FAFC; padding: 10px; border-radius: 12px;'>🟢 Unterrichtsrelevant &nbsp;|&nbsp; 🔴 Ablenkung &nbsp;|&nbsp; 🟡 Unsicher</div>", unsafe_allow_html=True)


# ==========================================
# 4. ANSICHT: SCHÜLER-DETAILANSICHT (HISTORIE)
# ==========================================
elif st.session_state.page == "student_detail":
    col_t1, col_t2, col_t3 = st.columns([6, 2, 2])
    with col_t1:
        if st.button("⬅️ Zurück zum Dashboard"):
            navigate_to("teacher_dashboard")
            st.rerun()
    with col_t2:
        st.empty()
    with col_t3:
        st.markdown("<div style='text-align: right;'><span class='room-badge'>Raum: 482 915</span></div>", unsafe_allow_html=True)
        
    st.markdown(f"### {st.session_state.selected_student} - Historie (Detaillierte Liste)")
    st.markdown("---")
    
    # Chronologische Liste der Aktivitäten
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
    st.markdown("<div style='text-align: center; background: #F8FAFC; padding: 10px; border-radius: 12px;'>🟢 Unterrichtsrelevant &nbsp;|&nbsp; 🔴 Ablenkung &nbsp;|&nbsp; 🟡 Unsicher</div>", unsafe_allow_html=True)


# ==========================================
# 5. ANSICHT: LEHRER-EINSTELLUNGEN
# ==========================================
elif st.session_state.page == "teacher_settings":
    col_t1, col_t2 = st.columns([8, 2])
    with col_t1:
        if st.button("⬅️ Zurück zum Dashboard"):
            navigate_to("teacher_dashboard")
            st.rerun()
    with col_t2:
        if st.button("🏠 Home"):
            navigate_to("home")
            st.rerun()
            
    st.markdown("### ⚙️ ClassWork AI: Einstellungen")
    st.markdown("---")
    
    # 1. Profil & Account
    with st.container(border=True):
        st.markdown("#### 👤 Profil & Account")
        st.write("Eingeloggt als: **Lehrer Max M.** (Schule Musterstadt)")
        if st.button("Profil bearbeiten"):
            st.toast("Profil-Bearbeitung geöffnet.")
            
    # 2. Systemeinstellungen
    with st.container(border=True):
        st.markdown("#### 🛠️ Systemeinstellungen")
        st.write("**Meldungs-Typen (🟢🔴🟡):** Aktiv")
        st.write("**Benachrichtigungen:** Push-Hinweise bei starker Ablenkung")
        st.markdown("---")
        st.markdown("**Geräte-Verwaltung:**")
        st.checkbox("Schülermodus automatisch erzwingen", value=True)
        st.checkbox("Strenger Datenschutz-Check aktiv", value=True)
        
    # 3. Datenschutz Regelungen
    with st.container(border=True):
        st.markdown("#### 🔒 Datenschutz Regelungen")
        st.write("Umfassende Datenschutz-Garantie: Lokale Analyse, keine Bildschirminhalte.")
        st.success("DSGVO Audit: Bestätigt 🟢")
        if st.button("Umfassende Regelungen ansehen"):
            st.info("Das System verarbeitet keinerlei Videostreams oder persönliche Inhalte extern.")
            
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 4. Logout / Abmelden
    if st.button("🚪 Logout / Abmelden", type="secondary"):
        navigate_to("home")
        st.rerun()
        
    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #A0AEC0; font-size: 12px;'>ClassWork AI v1.0 | DSGVO Audit Status: Erfolgreich</p>", unsafe_allow_html=True)
