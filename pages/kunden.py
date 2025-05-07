import streamlit as st
import psycopg2

# Datenbankverbindung
DATABASE_URL = st.secrets["database"]["url"]

# Kunden speichern
def save_kunde(name, adresse, objekt):
    conn = psycopg2.connect(DATABASE_URL)
    c = conn.cursor()
    c.execute('''
        INSERT INTO kunden (name, adresse, objekt)
        VALUES (%s, %s, %s)
    ''', (name, adresse, objekt))
    conn.commit()
    conn.close()

# Kunden abrufen
def get_kunden():
    conn = psycopg2.connect(DATABASE_URL)
    c = conn.cursor()
    c.execute("SELECT * FROM kunden ORDER BY name")
    kunden = c.fetchall()
    conn.close()
    return kunden

# Streamlit-Seite
st.set_page_config(page_title="Kundenverwaltung", layout="wide")
st.title("Kundenverwaltung")

# Kunden hinzufügen
st.subheader("Neuen Kunden hinzufügen")
with st.form(key="kunden_form"):
    name = st.text_input("Kundenname (z. B. Büro Müller)")
    adresse = st.text_input("Adresse (z. B. Hauptstr. 1, Berlin)", value="")
    objekt = st.text_input("Objektname für Zeiterfassung (z. B. Büro Müller Hauptstr.)")
    submit_button = st.form_submit_button("Kunden speichern")
    if submit_button:
        if name and objekt:
            save_kunde(name, adresse, objekt)
            st.success(f"Kunde {name} gespeichert!")
        else:
            st.error("Bitte Kundenname und Objektname ausfüllen!")

# Kunden anzeigen
st.subheader("Vorhandene Kunden")
kunden = get_kunden()
if kunden:
    st.table(kunden)  # Spalten: ID, Name, Adresse, Objekt
else:
    st.info("Keine Kunden vorhanden.")
