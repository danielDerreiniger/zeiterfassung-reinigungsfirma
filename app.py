import streamlit as st
import psycopg2

# Datenbankverbindung
DATABASE_URL = st.secrets["DATABASE_URL"]

# Funktion zum Testen der Datenbankverbindung
def test_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        st.success("Datenbankverbindung erfolgreich!")
        conn.close()
    except Exception as e:
        st.error(f"Fehler bei der Datenbankverbindung: {e}")

# Streamlit-App
st.title("Zeiterfassung Reinigungsfirma - Test")
st.write("Dies ist ein Test, um die Datenbankverbindung zu überprüfen.")
if st.button("Verbindung testen"):
    test_connection()
