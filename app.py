import streamlit as st

# Seiten-Konfiguration
st.set_page_config(
    page_title="ClassWork AI (Teachable Machine)",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialisierung des Session States für die Navigation
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
    st.markdown("### *Modell-Variante A: Eigenes Teachable-Machine-Modell*")
    st.markdown("Datenschutzfreundliche Aktivitätsmeldung für konzentriertes Lernen im Unterricht.")
    st.markdown("---")

    # Zwei Haupt-Buttons im Grid-Layout
    col1, col2 = st.columns(2)

    with col1:
        st.info("### Für Lehrkräfte")
        st.write("Erstelle einen Unterrichtsraum und behalte den Status der Klasse im Blick – basierend auf deinem individuell trainierten Modell.")
        st.button("🏫 Als Lehrer Raum hosten", on_click=go_to_teacher, use_container_width=True, type="primary")

    with col2:
        st.success("### Für Schülerinnen & Schüler")
        st.write("Tritt dem Raum deines Lehrers bei. Dein Bildschirm wird im Hintergrund automatisch und geschützt analysiert.")
        st.button("💻 Als Schüler Raum beitreten", on_click=go_to_student, use_container_width=True, type="primary")

    st.markdown("---")
    st.markdown("### ❓ Wie es funktioniert (Teachable Machine)")
    
    info_col1, info_col2, info_col3 = st.columns(3)
    with info_col1:
        st.markdown("**1. Raum beitreten**")
        st.caption("Schüler verbinden sich mit der Raum-ID des Lehrers.")
    with info_col2:
        st.markdown("**2. Lokale TM-Analyse**")
        st.caption("Das selbst trainierte Keras/TensorFlow-Modell klassifiziert die App-Screenshots.")
    with info_col3:
        st.markdown("**3. Status-Anzeige**")
        st.caption("Der Lehrer sieht ausschließlich den Farb-Status (Grün/Rot) im Dashboard.")


# ==========================================
# SEITE 2: LEHRER-DASHBOARD (HOST)
# ==========================================
elif st.session_state.page == "teacher":
    # Sidebar für Einstellungen (Getrennt für Teachable Machine)
    st.sidebar.title("⚙️ Lehrer-Steuerung")
    st.sidebar.button("⬅️ Zurück zum Hauptmenü", on_click=go_to_home)
    st.sidebar.markdown("---")
    
    st.sidebar.info("📌 **Aktive App-Version:**\nTeachable Machine (Eigenes Modell)")
    st.sidebar.markdown("---")
    st.sidebar.write("**Raum-ID:** `CLASS-TM-2026`")

    # Hauptinhalt Lehrer-Dashboard
    st.title("👨‍🏫 ClassWork AI – Lehrer-Dashboard")
    st.markdown("**Aktiver Raum:** `CLASS-TM-2026` | **KI:** *Teachable Machine (Custom Model)*")
    st.markdown("---")

    st.subheader("Übersicht der Klasse (Live-Status)")

    # Beispiel-Raster für Schüler-Kacheln
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### Max")
        st.success("🟢 **Status:** Unterrichtsrelevant")
        st.caption("Klasse: Unterricht (GoodNotes)")
        st.caption("Letztes Update: Vor 2 Sekunden")

    with col2:
        st.markdown("### Anna")
        st.error("🔴 **Status:** Ablenkung erkannt")
        st.caption("Klasse: Ablenkung (Spiel)")
        st.caption("Letztes Update: Vor 5 Sekunden")

    with col3:
        st.markdown("### Lukas")
        st.success("🟢 **Status:** Unterrichtsrelevant")
        st.caption("Klasse: Unterricht (Recherche)")
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
    room_id = st.text_input("Gib die Raum-ID deines Lehrers ein:", placeholder="z. B. CLASS-TM-2026")
    
    if st.button("Verbinden", type="primary"):
        if room_id:
            st.success(f"Erfolgreich mit Raum **{room_id}** verbunden!")
        else:
            st.warning("Bitte gib eine gültige Raum-ID ein.")

    st.markdown("---")
    st.subheader("2. Übertragungs-Status")
    
    st.info("🟢 **Status:** Aktiv & Verbunden")
    st.write("Deine Bildschirmaktivität wird im Hintergrund durch dein Teachable-Machine-Modell analysiert. Der Lehrer sieht **keine** Bildschirminhalte, sondern nur deinen Arbeitsstatus.")
