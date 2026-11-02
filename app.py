import streamlit as st

# Seiten-Konfiguration (Titel im Browser-Tab, Icon und breites Layout)
st.set_page_config(
    page_title="ClassWork AI",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialisierung des Session States für die Navigation (falls noch nicht gesetzt)
if "page" not in st.session_state:
    st.session_state.page = "home"

# Funktionen für Seitenwechsel
def go_to_teacher():
    st.session_state.page = "teacher"

def go_to_student():
    st.session_state.page = "student"

def go_to_home():
    st.session_state.page = "home"


# ==========================================
# SEITE 1: STARTBILDSCHIRM (HOME)
# ==========================================
if st.session_state.page == "home":
    st.title("🏫 ClassWork AI")
    st.subheader("Datenschutzfreundliche Aktivitätsmeldung für konzentriertes Lernen")
    st.markdown("---")

    # Zwei Haupt-Buttons im Grid-Layout
    col1, col2 = st.columns(2)

    with col1:
        st.info("### Für Lehrkräfte")
        st.write("Erstelle einen Unterrichtsraum und behalte den Status der Klasse im Blick, ohne die Bildschirme der Schüler einzusehen.")
        st.button("🏫 Als Lehrer Raum hosten", on_click=go_to_teacher, use_container_width=True, type="primary")

    with col2:
        st.success("### Für Schülerinnen & Schüler")
        st.write("Tritt dem Raum deines Lehrers bei. Dein Bildschirm wird automatisch und geschützt im Hintergrund analysiert.")
        st.button("💻 Als Schüler Raum beitreten", on_click=go_to_student, use_container_width=True, type="primary")

    st.markdown("---")
    st.markdown("### ❓ Wie es funktioniert")
    
    info_col1, info_col2, info_col3 = st.columns(3)
    with info_col1:
        st.markdown("**1. Raum beitreten**")
        st.caption("Schüler treten mit einer Raum-ID bei und starten die automatische Übertragung.")
    with info_col2:
        st.markdown("**2. KI-Analyse**")
        st.caption("Die KI erkennt lokal/geschützt den Typ der genutzten App (z.B. Notizen vs. Spiel).")
    with info_col3:
        st.markdown("**3. Status-Anzeige**")
        st.caption("Der Lehrer sieht nur einen Farb-Status (Grün/Rot) – die Privatsphäre bleibt geschützt.")


# ==========================================
# SEITE 2: LEHRER-DASHBOARD (HOST)
# ==========================================
elif st.session_state.page == "teacher":
    # Sidebar für Einstellungen
    st.sidebar.title("⚙️ Einstellungen")
    st.sidebar.button("⬅️ Zurück zum Hauptmenü", on_click=go_to_home)
    st.sidebar.markdown("---")
    
    st.sidebar.subheader("KI-Modell Auswahl")
    model_choice = st.sidebar.radio(
        "Wähle das Modell für die Auswertung:",
        ("Teachable Machine (Eigenes Modell)", "Vortrainiertes Modell (Hugging Face)"),
        index=0
    )
    
    st.sidebar.markdown("---")
    st.sidebar.write("**Raum-ID:** `CLASS-10B-2026`")

    # Hauptinhalt Lehrer-Dashboard
    st.title("👨‍🏫 ClassWork AI – Lehrer-Dashboard")
    st.markdown(f"**Aktiver Raum:** `CLASS-10B-2026` | **Modell:** *{model_choice}*")
    st.markdown("---")

    st.subheader("Übersicht der Klasse (Live-Status)")

    # Beispiel-Raster für Schüler-Kacheln
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### Max")
        st.success("🟢 **Status:** Aufgabenbezogen")
        st.caption("Erkannte App: GoodNotes / Notizen")
        st.caption("Letztes Update: Vor 2 Sekunden")

    with col2:
        st.markdown("### Anna")
        st.error("🔴 **Status:** Ablenkung erkannt")
        st.caption("Erkannte App: Spiel / Social Media")
        st.caption("Letztes Update: Vor 5 Sekunden")

    with col3:
        st.markdown("### Lukas")
        st.success("🟢 **Status:** Aufgabenbezogen")
        st.caption("Erkannte App: Safari (Recherche)")
        st.caption("Letztes Update: Vor 1 Sekunde")


# ==========================================
# SEITE 3: SCHÜLER-ANSICHT (BEITRETEN)
# ==========================================
elif st.session_state.page == "student":
    st.sidebar.button("⬅️ Zurück zum Hauptmenü", on_click=go_to_home)
    
    st.title("💻 ClassWork AI – Schüler-Ansicht")
    st.markdown("---")

    # Formular zum Beitreten
    st.subheader("1. Raum-ID eingeben")
    room_id = st.text_input("Gib die Raum-ID deines Lehrers ein:", placeholder="z. B. CLASS-10B-2026")
    
    if st.button("Verbinden", type="primary"):
        if room_id:
            st.success(f"Erfolgreich mit Raum **{room_id}** verbunden!")
        else:
            st.warning("Bitte gib eine gültige Raum-ID ein.")

    st.markdown("---")
    st.subheader("2. Übertragungs-Status")
    
    # Vorschau auf den aktiven Status des Schülers
    st.info("🟢 **Status:** Aktiv & Verbunden")
    st.write("Deine Bildschirmaktivität wird im Hintergrund geschützt analysiert. Der Lehrer sieht **keinen** Bildschirminhalt, sondern nur deinen Arbeitsstatus.")
