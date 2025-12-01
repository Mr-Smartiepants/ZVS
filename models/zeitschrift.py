# Datenbankmodell für Zeitschriften

import mysql.connector
from . import get_db_connection
from datetime import datetime
from flask import jsonify
from models.user import User

def add_zeitschrift(titel):
    """Fügt eine neue Zeitschrift (nur Titel) hinzu."""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                'INSERT INTO zeitschriften (Titel) VALUES (%s)',
                (titel,)
            )
            conn.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Fehler beim Hinzufügen der Zeitschrift: {err}")
            return False
        finally:
            cursor.close()
            conn.close()
    return False

def get_all_zeitschriften():
    """Gibt alle Zeitschriften zurück."""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT 
                z.ZeitschriftID,
                z.Titel,
                COUNT(DISTINCT e.ExemplarID) as exemplar_count,
                SUM(CASE WHEN a.Rueckgabedatum IS NULL THEN 1 ELSE 0 END) as ausgeliehen_count
            FROM zeitschriften z
            LEFT JOIN exemplare e ON z.ZeitschriftID = e.ZeitschriftID AND e.Aktiv = 1
            LEFT JOIN ausleihen a ON e.ExemplarID = a.ExemplarID
            GROUP BY z.ZeitschriftID
        ''')
        zeitschriften = cursor.fetchall() if cursor else []
        cursor.close()
        conn.close()
        return zeitschriften
    return []

def get_zeitschrift_by_id(zeitschrift_id):
    """Holt eine Zeitschrift mit allen zugehörigen Exemplaren."""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT 
                z.ZeitschriftID,
                z.Titel
            FROM zeitschriften z
            WHERE z.ZeitschriftID = %s
        ''', (zeitschrift_id,))
        zeitschrift = cursor.fetchone()
        cursor.close()
        conn.close()
        return zeitschrift
    return None

def delete_zeitschrift(zeitschrift_id):
    """Löscht eine Zeitschrift (und alle zugehörigen Exemplare)."""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            # Zuerst alle Exemplare dieser Zeitschrift inaktiv setzen
            cursor.execute(
                'UPDATE exemplare SET Aktiv = 0 WHERE ZeitschriftID = %s',
                (zeitschrift_id,)
            )
            # Dann die Zeitschrift löschen
            cursor.execute(
                'DELETE FROM zeitschriften WHERE ZeitschriftID = %s',
                (zeitschrift_id,)
            )
            conn.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Fehler beim Löschen der Zeitschrift: {err}")
            return False
        finally:
            cursor.close()
            conn.close()
    return False

def top_5_zeitschriften():
    """Gibt die 5 am häufigsten ausgeliehenenen Zeitschriften zurück."""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT 
                z.Titel,
                COUNT(a.AusleiheID) as anzahl_ausleihen
            FROM zeitschriften z
            LEFT JOIN exemplare e ON z.ZeitschriftID = e.ZeitschriftID
            LEFT JOIN ausleihen a ON e.ExemplarID = a.ExemplarID
            GROUP BY z.ZeitschriftID
            ORDER BY anzahl_ausleihen DESC
            LIMIT 5
        ''')
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
    return []

def verfuegbare_exemplare():
    """Gibt Anzahl verfügbarer Exemplare zurück."""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT COUNT(*) as count FROM exemplare e
            WHERE e.Aktiv = 1 
            AND e.ExemplarID NOT IN (
                SELECT DISTINCT ExemplarID FROM ausleihen WHERE Rueckgabedatum IS NULL
            )
        ''')
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row[0] if row else 0
    return 0

def ausgeliehene_exemplare():
    """Gibt Anzahl ausgeliehenener Exemplare zurück."""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT COUNT(DISTINCT ExemplarID) as count FROM ausleihen 
            WHERE Rueckgabedatum IS NULL
        ''')
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row[0] if row else 0
    return 0