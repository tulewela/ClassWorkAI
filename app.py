import streamlit as st
import random
import os
from datetime import datetime
from PIL import Image
from transformers import pipeline

# 1. Seitengestaltung & Fix gegen Scrollen auf Startseite
st.set_page_config(
    page_title="ClassWork AI",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Custom CSS für den perfekten Startbildschirm & normale Unterseiten (Unangetastet!)
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

# HUGGING FACE KI-MODELL LADEN (Einmalig gecacht für maximale Geschwindigkeit)
@st.cache_resource
def load_ai_classifier():
    return pipeline("zero-shot-image-classification", model="openai/clip-vit-base-patch32")

# Detaillierte KI-Klassifizierungs-Logik
def classify_student_screen(image: Image.Image):
    classifier = load_ai_classifier()
    
    # Sehr ausführliche Beschreibungen für höchste Erkennungsgenauigkeit
    label_relevant = (
        "digital school notes, handwritten tablet notes, Goodnotes, Notability, OneNote, "
        "Microsoft Word document, Google Docs text editor, PowerPoint presentation slides, "
        "PDF worksheet, textbook page, math equations, geometry, school assignment, "
        "coding IDE, programming environment, calculator app, spreadsheet table, learning platform"
    )
    
    label_distraction = (
        "video game gameplay, Minecraft, Fortnite, Roblox, mobile game, gaming screen, "
        "social media feed, TikTok, Instagram, Snapchat, YouTube entertainment video, "
        "Netflix movie or series streaming, WhatsApp or Discord chat messages, "
        "online shopping store, sports live stream, memes, comic or entertainment website"
    )
    
    label_research = (
        "Google search engine results page, Bing search, Wikipedia encyclopedia article, "
        "online dictionary, DeepL or Google Translate, educational news article, "
        "scientific blog, informational website with text paragraphs, library catalog, "
        "browser tabs with academic or factual information research"
    )
    
    label_unsure = (
        "empty desktop wallpaper, lock screen, home screen with app icons, "
        "system settings menu, file explorer folder, blurry screen, "
        "loading screen, login window, blank white or black screen"
    )
    
    candidate_labels = [label_relevant, label_distraction, label_research, label_unsure]
    results = classifier(image, candidate_labels=candidate_labels)
    
    top_label = results[0]["label"]
    top_score = results[0]["score"]
    
    # Wenn die KI sich unsicher ist (Score unter 42%), automatisch auf "Unsicher" setzen
    if top_score < 0.42 or top_label == label_unsure:
        return "yellow", "Unsicher", top_score
    elif top_label == label_relevant:
        return "green", "Unterrichtsrelevant", top_score
    elif top_label == label_distraction:
        return "red", "Ablenkung", top_score
    elif top_label == label_research:
        return "orange", "Recherche", top_score
    else:
        return "yellow", "Unsicher", top_score

# GEMEINSAMER SERVER-SPEICHER für Räume & Schüler-Daten über alle Tabs hinweg
@st.cache_resource
def get_shared_rooms():
    return {}

shared_rooms = get_shared_rooms()

# Session State Initialisierung
if "page" not in st.session_state:
    st.session_state.page = "home"

if "teacher_room_code" not in st.session_state:
    st.session_state.teacher_room_code = None

if "student_joined_room" not in st.session_state:
    st.session_state.student_joined_room = None

if "student_joined_name" not in st.session_state:
    st.session_state.student_joined_name = None

if "confirm_close" not in st.session_state:
    st.session_state.confirm_close = False

if "selected_student" not in st.session_state:
    st.session_state.selected_student = None

# Query Parameters am Anfang abfangen
query_params = st.query_params
if "nav" in query_params:
    st.session_state.page = query_params["nav"]

if "action" in query_params and query_params["action"] == "host":
    if not st.session_state.teacher_room_code or st.session_state.teacher_room_code not in shared_rooms:
        new_code = str(random.randint(100000, 999999))
        while new_code in shared_rooms:
            new_code = str(random.randint(100000, 999999))
        shared_rooms[new_code] = {}
        st.session_state.teacher_room_code = new_code
    
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
# 2. SCHÜLER-ANSICHT (RAUM BEITRETEN & KI-TEST)
# ==========================================
elif st.session_state.page == "student_join":
    col_t1, col_t2, col_t3 = st.columns([1, 8, 2])
    with col_t1:
        render_logo(width=50)
    with col_t2:
        st.markdown("<h2 style='margin:0; font-size: 22px; line-height: 50px;'>ClassWork AI: Schüler-Ansicht</h2>", unsafe_allow_html=True)
    with col_t3:
        if st.button("🏠 Home", key="home_btn_1"):
            st.session_state.student_joined_room = None
            st.session_state.student_joined_name = None
            navigate_to("home")
            
    st.markdown("---")
    
    _, form_col, _ = st.columns([1, 1.4, 1])
    with form_col:
        st.markdown("<br>", unsafe_allow_html=True)
        
        is_connected = (
            st.session_state.student_joined_room is not None 
            and st.session_state.student_joined_room in shared_rooms
            and st.session_state.student_joined_name in shared_rooms[st.session_state.student_joined_room]
        )

        if not is_connected:
            with st.container(border=True):
                st.markdown("### Raum beitreten")
                entered_code = st.text_input("Raum-Code", placeholder="Gib den 6-stelligen Raum-Code ein", max_chars=6, label_visibility="collapsed")
                student_name = st.text_input("Dein Name", placeholder="Dein Vorname (z.B. Alex)")
                
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Raum beitreten", key="submit_join"):
                    user_code = entered_code.strip()
                    clean_name = student_name.strip()
                    
                    if user_code in shared_rooms:
                        if clean_name:
                            now_str = datetime.now().strftime("%H:%M:%S")
                            if clean_name not in shared_rooms[user_code]:
                                shared_rooms[user_code][clean_name] = {
                                    "status": "green",
                                    "status_text": "Unterrichtsrelevant",
                                    "last_update": f"Beigetreten ({now_str})",
                                    "history": [
                                        (now_str, "green", "Unterrichtsrelevant", "Raum beigetreten (Startstatus)")
                                    ]
                                }
                            st.session_state.student_joined_room = user_code
                            st.session_state.student_joined_name = clean_name
                            st.rerun()
                        else:
                            st.warning("Bitte gib deinen Namen ein.")
                    elif not user_code:
                        st.warning("Bitte gib den 6-stelligen Raum-Code ein.")
                    else:
                        st.error("Falscher Raum-Code. Es ist kein aktiver Raum mit diesem Code gefunden worden.")
        else:
            r_code = st.session_state.student_joined_room
            s_name = st.session_state.student_joined_name
            
            with st.container(border=True):
                st.success(f"Verbunden mit Raum **{r_code}** als **{s_name}**")
                st.markdown("#### 📸 Aktivitäts-Check (KI-Test)")
                st.caption("Lade einen Screenshot (z.B. Goodnotes, Google, Spiel oder Desktop) hoch, um die KI-Erkennung zu testen.")
                
                uploaded_file = st.file_uploader("Bild auswählen", type=["png", "jpg", "jpeg"], label_visibility="collapsed")
                
                if uploaded_file is not None:
                    image = Image.open(uploaded_file).convert("RGB")
                    # Korrigierter Parameter use_column_width für Streamlit 1.35.0
                    st.image(image, caption="Vorschau (wird NICHT an den Lehrer gesendet)", use_column_width=True)
                    
                    if st.button("🔍 Jetzt mit KI analysieren", key="analyze_btn"):
                        with st.spinner("KI analysiert Aktivität lokal..."):
                            color_code, status_label, confidence = classify_student_screen(image)
                            now_str = datetime.now().strftime("%H:%M:%S")
                            
                            dot_map = {"green": "🟢", "red": "🔴", "orange": "🟠", "yellow": "🟡"}
                            dot = dot_map.get(color_code, "🟡")
                            
                            if r_code in shared_rooms and s_name in shared_rooms[r_code]:
                                shared_rooms[r_code][s_name]["status"] = color_code
                                shared_rooms[r_code][s_name]["status_text"] = status_label
                                shared_rooms[r_code][s_name]["last_update"] = f"Um {now_str}"
                                shared_rooms[r_code][s_name]["history"].insert(
                                    0, (now_str, color_code, status_label, f"KI-Konfidenz: {int(confidence * 100)}%")
                                )
                            
                            st.info(f"**Ergebnis:** {dot} **{status_label}** (Sicherheit: {int(confidence * 100)}%) — Status wurde an das Lehrer-Dashboard übermittelt!")

                st.markdown("---")
                if st.button("Raum verlassen", key="leave_room_student"):
                    st.session_state.student_joined_room = None
                    st.session_state.student_joined_name = None
                    st.rerun()
                    
        st.markdown("<br>", unsafe_allow_html=True)
        st.info("🔒 **Deine Privatsphäre ist geschützt.** Es werden keine Bilder an den Lehrer übertragen – nur der Status-Punkt.")


# ==========================================
# 3. LEHRER-DASHBOARD (KLASSENÜBERSICHT)
# ==========================================
elif st.session_state.page == "teacher_dashboard":
    if not st.session_state.teacher_room_code or st.session_state.teacher_room_code not in shared_rooms:
        new_code = str(random.randint(100000, 999999))
        while new_code in shared_rooms:
            new_code = str(random.randint(100000, 999999))
        shared_rooms[new_code] = {}
        st.session_state.teacher_room_code = new_code

    display_code = st.session_state.teacher_room_code

    col_t1, col_t2, col_t3, col_t4, col_t5 = st.columns([0.8, 3.8, 2, 1.8, 1.6])
    with col_t1:
        render_logo(width=50)
    with col_t2:
        st.markdown("<h2 style='margin:0; font-size: 22px; line-height: 50px;'>ClassWork AI: Lehrer-Dashboard</h2>", unsafe_allow_html=True)
    with col_t3:
        if st.button("⚙️ Einstellungen", key="settings_btn"):
            navigate_to("teacher_settings")
    with col_t4:
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
                    if display_code in shared_rooms:
                        del shared_rooms[display_code]
                    st.session_state.teacher_room_code = None
                    st.session_state.confirm_close = False
                    navigate_to("home")
            with c_nein:
                if st.button("Nein", key="no_close"):
                    st.session_state.confirm_close = False
                    st.rerun()
        st.markdown("<br>", unsafe_allow_html=True)

    students_dict = shared_rooms.get(display_code, {})
    student_names = list(students_dict.keys())

    # Aktualisieren-Button Bereich
    c_head1, c_head2 = st.columns([5, 1.5])
    with c_head1:
        st.subheader(f"Verbundene Schüler ({len(student_names)})")
    with c_head2:
        if st.button("🔄 Aktualisieren", key="refresh_dashboard"):
            st.rerun()

    if not student_names:
        st.info(f"Der Raum `{display_code}` ist aktuell noch leer. Teile den 6-stelligen Code mit deinen Schülerinnen und Schülern, damit sie beitreten können.")
    else:
        dot_map = {"green": "🟢", "red": "🔴", "orange": "🟠", "yellow": "🟡"}
        
        for i in range(0, len(student_names), 3):
            cols = st.columns(3)
            for j in range(3):
                idx = i + j
                if idx < len(student_names):
                    name = student_names[idx]
                    s_data = students_dict[name]
                    dot = dot_map.get(s_data["status"], "🟢")
                    
                    with cols[j]:
                        with st.container(border=True):
                            c1, c2 = st.columns([4, 1])
                            with c1:
                                st.markdown(f"**{name}**")
                            with c2:
                                st.markdown(f"<div style='text-align: right;'>{dot}</div>", unsafe_allow_html=True)
                            
                            st.markdown("<div style='text-align: center; padding: 15px 0;'><span style='font-size: 36px;'>👤</span></div>", unsafe_allow_html=True)
                            
                            bc1, bc2 = st.columns([2.2, 1.8])
                            with bc1:
                                st.caption(f"{s_data['status_text']} • {s_data['last_update']}")
                            with bc2:
                                if st.button("Details", key=f"btn_detail_{name}"):
                                    st.session_state.selected_student = name
                                    navigate_to("student_detail")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center; background: #F8FAFC; padding: 12px; border-radius: 14px; font-weight: 500;'>🟢 Unterrichtsrelevant &nbsp;|&nbsp; 🔴 Ablenkung &nbsp;|&nbsp; 🟠 Recherche &nbsp;|&nbsp; 🟡 Unsicher</div>", unsafe_allow_html=True)


# ==========================================
# 4. SCHÜLER
