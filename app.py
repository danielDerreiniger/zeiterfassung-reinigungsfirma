import streamlit as st
import psycopg2
from datetime import datetime

# Datenbankverbindung
DATABASE_URL = st.secrets["database"]["url"]

# Datenbank initialisieren
def init_db():
    conn = psycopg2.connect(DATABASE_URL)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS zeiten (
            id SERIAL PRIMARY KEY,
            mitarbeiter TEXT,
            objekt TEXT,
            start_zeit TEXT,
            end_zeit TEXT,
            pause_minuten INTEGER DEFAULT 0
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS kunden (
            id SERIAL PRIMARY KEY,
            name TEXT,
            adresse TEXT,
            objekt TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Zeit speichern
def save_zeit(mitarbeiter, objekt, start_zeit, end_zeit=None, pause_minuten=0):
    conn = psycopg2.connect(DATABASE_URL)
    c = conn.cursor()
    c.execute('''
        INSERT INTO zeiten (mitarbeiter, objekt, start_zeit, end_zeit, pause_minuten)
        VALUES (%s, %s, %s, %s, %s) RETURNING id
    ''', (mitarbeiter, objekt, start_zeit, end_zeit, pause_minuten))
    zeit_id = c.fetchone()[0]
    conn.commit()
    conn.close()
    return zeit_id

# Zeit aktualisieren
def update_zeit(zeit_id, end_zeit):
    conn = psycopg2.connect(DATABASE_URL)
    c = conn.cursor()
    c.execute('''
        UPDATE zeiten SET end_zeit = %s WHERE id = %s
    ''', (end_zeit, zeit_id))
    conn.commit()
    conn.close()

# Zeiten abrufen
def get_zeiten(mitarbeiter=None):
    conn = psycopg2.connect(DATABASE_URL)
    c = conn.cursor()
    if mitarbeiter:
        c.execute("SELECT * FROM zeiten WHERE mitarbeiter = %s ORDER BY start_zeit DESC", (mitarbeiter,))
    else:
        c.execute("SELECT * FROM zeiten ORDER BY start_zeit DESC")
    zeiten = c.fetchall()
    conn.close()
    return zeiten

# Kunden abrufen
def get_kunden():
    conn = psycopg2.connect(DATABASE_URL)
    c = conn.cursor()
    c.execute("SELECT objekt FROM kunden ORDER BY objekt")
    kunden = [row[0] for row in c.fetchall()]
    conn.close()
    return kunden

# Streamlit-App
st.set_page_config(page_title="Zeiterfassung Reinigungsfirma", layout="wide")
st.title("Zeiterfassung für [Dein Firmenname]")

# Session-State
if "zeit_running" not in st.session_state:
    st.session_state.zeit_running = False
    st.session_state.zeit_id = None
    st.session_state.start_zeit = None
    st.session_state.objekt = None

# Sidebar-Menü
menu = ["Zeit erfassen", "Berichte", "Kundenverwaltung"]
choice = st.sidebar.selectbox("Menü", menu)

if choice == "Zeit erfassen":
    st.subheader("Arbeitszeit erfassen")
    mitarbeiter = st.text_input("Mitarbeitername")
    kunden = get_kunden()
    objekt = st.selectbox("Objekt", kunden if kunden else ["Keine Objekte vorhanden"])

    if not st.session_state.zeit_running:
        if st.button("Start"):
            if mitarbeiter and objekt and objekt != "Keine Objekte vorhanden":
                start_zeit = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                zeit_id = save_zeit(mitarbeiter, objekt, start_zeit)
                st.session_state.zeit_running = True
                st.session_state.zeit_id = zeit_id
                st.session_state.start_zeit = start_zeit
                st.session_state.objekt = objekt
                st.success(f"Zeit gestartet für {objekt} um {start_zeit}")
            else:
                st.error("Bitte Mitarbeitername und gültiges Objekt auswählen!")
    else:
        st.write(f"Laufende Zeit: {st.session_state.objekt} (Start: {st.session_state.start_zeit})")
        if st.button("Stop"):
            end_zeit = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            update_zeit(st.session_state.zeit_id, end_zeit)
            st.session_state.zeit_running = False
            st.session_state.zeit_id = None
            st.session_state.start_zeit = None
            st.session_state.objekt = None
            st.success(f"Zeit gestoppt um {end_zeit}")

elif choice == "Berichte":
    st.subheader("Zeiterfassungs-Berichte")
    mitarbeiter_filter = st.text_input("Mitarbeitername für Filter (optional)")
    zeiten = get_zeiten(mitarbeiter_filter if mitarbeiter_filter else None)
    if zeiten:
        st.table(zeiten)  # Spalten: ID, Mitarbeiter, Objekt, Start, Ende, Pause
    else:
        st.info("Keine Daten vorhanden.")

elif choice == "Kundenverwaltung":
    st.write("Wechsle zur Kundenverwaltung über das Menü oder direkt oben.")
