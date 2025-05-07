import streamlit as st
import sqlite3
from datetime import datetime

# Datenbank initialisieren
def init_db():
    conn = sqlite3.connect("zeiterfassung.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS zeiten (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mitarbeiter TEXT,
            objekt TEXT,
            start_zeit TEXT,
            end_zeit TEXT,
            pause_minuten INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# Zeit speichern
def save_zeit(mitarbeiter, objekt, start_zeit, end_zeit, pause_minuten=0):
    conn = sqlite3.connect("zeiterfassung.db")
    c = conn.cursor()
    c.execute('''
        INSERT INTO zeiten (mitarbeiter, objekt, start_zeit, end_zeit, pause_minuten)
        VALUES (?, ?, ?, ?, ?)
    ''', (mitarbeiter, objekt, start_zeit, end_zeit, pause_minuten))
    conn.commit()
    conn.close()

# Zeiten abrufen
def get_zeiten():
    conn = sqlite3.connect("zeiterfassung.db")
    c = conn.cursor()
    c.execute("SELECT * FROM zeiten")
    zeiten = c.fetchall()
    conn.close()
    return zeiten

# Streamlit-App
st.set_page_config(page_title="Zeiterfassung Reinigungsfirma", layout="wide")
st.title("Zeiterfassung für Reinigungsfirma")

# Sidebar-Menü
menu = ["Zeit erfassen", "Berichte"]
choice = st.sidebar.selectbox("Menü", menu)

if choice == "Zeit erfassen":
    st.subheader("Arbeitszeit erfassen")
    mitarbeiter = st.text_input("Mitarbeitername")
    objekt = st.selectbox("Objekt", ["Kunde A", "Kunde B", "Kunde C"])  # Anpassen
    start_zeit = st.time_input("Startzeit")
    end_zeit = st.time_input("Endzeit")
    pause_minuten = st.number_input("Pausen (in Minuten)", min_value=0, value=0)
    
    if st.button("Zeit speichern"):
        start_zeit_str = start_zeit.strftime("%H:%M")
        end_zeit_str = end_zeit.strftime("%H:%M")
        save_zeit(mitarbeiter, objekt, start_zeit_str, end_zeit_str, pause_minuten)
        st.success("Zeit gespeichert!")

elif choice == "Berichte":
    st.subheader("Zeiterfassungs-Berichte")
    zeiten = get_zeiten()
    if zeiten:
        st.table(zeiten)  # Einfache Tabellenanzeige
    else:
        st.info("Keine Daten vorhanden.")
