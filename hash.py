import sys
import os
import bcrypt
import mysql.connector
from app import app
from models import get_db_connection

# Flask-Anwendungskontext aktivieren
with app.app_context():
    # Verbindungslogik zur Datenbank
    conn = get_db_connection()

    cursor = conn.cursor(dictionary=True)

    # Alle Benutzer und Passwörter abfragen
    cursor.execute("SELECT id, password FROM benutzer")
    benutzer = cursor.fetchall()

    # Durch alle Benutzer iterieren und die Passwörter hashen
    for user in benutzer:
        klartext_password = user['password']  # Klartext-Passwort
        hashed_password = bcrypt.hashpw(klartext_password.encode('utf-8'), bcrypt.gensalt())  # Passwort hashen

        # Aktualisiere die Tabelle mit dem gehashten Passwort
        cursor.execute("UPDATE benutzer SET password = %s WHERE id = %s", (hashed_password.decode('utf-8'), user['id']))

    # Änderungen in der Datenbank speichern
    conn.commit()

    cursor.close()
    conn.close()

    print("Alle Passwörter erfolgreich gehasht und aktualisiert.")
