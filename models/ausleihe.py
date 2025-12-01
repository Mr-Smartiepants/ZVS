# Datenbankmodell f+r Ausleihen

import mysql.connector
from . import get_db_connection
from datetime import datetime
from flask import jsonify
from models.user import User

def ausleihe_erstellen(exemplar_id, benutzer_id):
    """eine neue Ausleihe erstellen.."""
    conn = get_sb_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            """checken ob bereits ausgeliehen"""
            cursor.execute(
                '''
                SELECT COUNT(*) as count FROM ausleihen
                WHERE ExemplarID = %s AND Rueckgabedatum IS NULL
                ''', (exemplar_id,))
            result = cursor.fetchone()
            if result and result['count'] > 0:
                return False, "Exemplar ist bereits ausgeliehen."
            
            """neue Ausleihe erstellen"""
            cursor.execute(
                '''
                INSERT INTO ausleihen (ExemplarID, BenutzerID, Ausleihdatum)
                VALUES (%s, %s, NOW())
                ''', (exemplar_id, benutzer_id))
            conn.commit()
            return True, "Ausleihe erfolgreich."
        except mysql.connector.Error as err:
            print(f"Fehler beim Erstellen der Ausleihe: {err}")
            return False, str(err)
        finally:
            cursor.close()
            conn.close()
    return False, "Datenbankverbindung fehlgeschlagen."

def rueckgabe_erstellen(exemplar_id, benutzer_id):
    """Rückgabe registrieren."""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                '''
                UPDATE ausleihen
                SET Rueckgabedatum = NOW()
                WHERE ExemplarID = %s AND BenutzerID = %s AND Rueckgabedatum IS NULL
                ''', (exemplar_id, benutzer_id))
            conn.commit()
            if cursor.rowcount > 0:
                return True, "Rückgabe erfolgreich."
            else:
                return False, "Keine offene Ausleihe gefunden."
        except mysql.connector.Error as err:
            print(f"Fehler bei der Rückgabe: {err}")
            return False, str(err)
        finally:
            cursor.close()
            conn.close()
    return False, "Datenbankverbindung fehlgeschlagen."

def get_aktuelle_ausleihen():
    """aktuelle Ausleihen zurückgeben."""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            '''
            SELECT
                a.AusleiheID,
                e.Barcode,
                z.Titel,
                e.AusgabeHeftnummer,
                b.firstname,
                b.name,
                a.Ausleihdatum
            FROM ausleihen a
            JOIN exemplare e ON a.ExemplarID = e.ExemplarID
            JOIN zeitschriften z ON e.ZeitschriftID = z.ZeitschriftID
            JOIN benutzer b ON a.BenutzerID = b.id
            WHERE a.Rueckgabedtatum IS NULL
            ORDER BY a.Ausleihdatum DESC
            '''
        )
        ausleihen = cursor.fetchall()
        cursor.close()
        conn.close()
        return ausleihen
    return []

def get_ausleihen_by_benutzer(benutzer_id):
    """Ausgabe aller Ausleihen eines Benutzers (offen und geschlossen)."""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            '''
            SELECT
                a.AusleiheID,
                z.Titel,
                e.AusgabeHeftnummer,
                a.Ausleihdatum,
                a.Rueckgabedatum
            FROM ausleihen a
            JOIN exemplare e ON a.ExemplarID = e.ExemplarID
            JOIN zeitschriften z ON e.ZeitschriftID = z.ZeitschriftID
            WHERE a.BenutzerID = %s
            ORDER BY a.AUsleihdatum DESC 
            ''', (benutzer_id,))
        ausleihen = cursor.fetchall()
        cursor.close()
        conn.close()
        return ausleihen
    return []

