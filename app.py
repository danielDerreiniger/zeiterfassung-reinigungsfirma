import streamlit as st
import psycopg2
from datetime import datetime

# Datenbankverbindung
DATABASE_URL = st.secrets["DATABASE_URL"]

# Funktion zum Abrufen der Kunden
def get_kunden():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("SELECT * FROM kunden")
        kunden = cur.fetchall()
        cur.close()
        conn.close()
        return kunden
    except Exception as e:
        st.error(f"Fehler bei der Datenbankverbindung: {e}")
        return []

# Funktion zum Hinzufügen eines Kunden
def add_kunde(name):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("INSERT INTO kunden (name) VALUES (%s) RETURNING id", (name,))
        new_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        st.success(f"Kunde {name} (ID: {new_id}) hinzugefügt!")
        return new_id
    except Exception as e:
        st.error(f"Fehler beim Hinzufügen des Kunden: {e}")
        return None

# Funktion zum Abrufen der Zeiten
def get_zeiten():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("SELECT * FROM zeiten")
        zeiten = cur.fetchall()
        cur.close()
        conn.close()
        return zeiten
    except Exception as e:
        st.error(f"Fehler beim Abrufen der Zeiten: {e}")
        return []

# Funktion zum Erfassen einer Zeit
def add_zeit(kunde_id, startzeit, endzeit):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("INSERT INTO zeiten (kunde_id, startzeit, endzeit) VALUES (%s, %s, %s)", (kunde_id, startzeit, endzeit))
        conn.commit()
        cur.close()
        conn.close()
        st.success("Zeit erfasst!")
    except Exception as e:
        st.error(f"Fehler beim Erfassen der Zeit: {e}")

# Streamlit-App
st.title("Zeiterfassung Reinigungsfirma")

# Kundenverwaltung
st.header("Kundenverwaltung")
kunden = get_kunden()
if kunden:
    st.write("Bestehende Kunden:")
    for kunde in kunden:
        st.write(f"- {kunde[1]} (ID: {kunde[0]})")
else:
    st.write("Keine Kunden gefunden.")

new_kunde = st.text_input("Neuer Kunde:")
if st.button("Kunde hinzufügen"):
    if new_kunde:
        add_kunde(new_kunde)

# Zeit erfassen
st.header("Zeit erfassen")
if kunden:
    selected_kunde = st.selectbox("Wähle einen Kunden:", [(kunde[0], kunde[1]) for kunde in kunden], format_func=lambda x: x[1])
    startzeit = st.time_input("Startzeit")
    endzeit = st.time_input("Endzeit")
    if st.button("Zeit erfassen"):
        start_dt = datetime.combine(datetime.today(), startzeit)
        end_dt = datetime.combine(datetime.today(), endzeit)
        add_zeit(selected_kunde[0], start_dt, end_dt)
else:
    st.write("Bitte füge zuerst einen Kunden hinzu.")

# Zeiten anzeigen
st.header("Erfasste Zeiten")
zeiten = get_zeiten()
if zeiten:
    for zeit in zeiten:
        st.write(f"Kunde ID: {zeit[1]}, Start: {zeit[2]}, Ende: {zeit[3]}")
else:
    st.write("Keine Zeiten erfasst.")
