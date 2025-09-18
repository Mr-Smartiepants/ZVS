# Datenbankmodell für Zeitschriften

import mysql.connector
from . import get_db_connection
from datetime import datetime
from flask import jsonify
from models.user import User

def add_zeitschrift(titel, barcode, ausgabe, erscheinungsdatum):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                '''
                INSERT INTO zeitschriften (titel, ausgabe, erscheinungsdatum, barcode, aktiv)
                VALUES (%s, %s, %s, %s, 1)
                ''',
                (titel, ausgabe, erscheinungsdatum, barcode)
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
    # alle aktiven  Zeitschriften von Datenbank abrufen + Verfügbarkeitsstatus
      
    conn = get_db_connection()

    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM zeitschriften WHERE aktiv = 1')
        zeitschriften = cursor.fetchall() if cursor else []
        if zeitschriften is None:
            zeitschriften = []

        # Verfügbarkeitsstatus hinzufügen
        for zeitschrift in zeitschriften:
            if zeitschrift['benutzer_id'] is None:
                zeitschrift['verfuegbar'] = True
            else:
                zeitschrift['verfuegbar'] = False

        if cursor:
            cursor.close()
        if conn:
            conn.close()
        return zeitschriften
    return [] # Leere Liste ausgeben wenn keine Verbindung zur DB hergestellt werden konnte

def update_zeitschrift(zeitschrift_id, neuer_titel=None, neue_ausgabe=None, neues_erscheinungsdatum=None, neuer_benutzer_id=None):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            sql_parts = []
            values = []

            if neuer_titel is not None:
                sql_parts.append("titel = %s")
                values.append(neuer_titel)
            if neue_ausgabe is not None:
                sql_parts.append("ausgabe = %s")
                values.append(neue_ausgabe)
            if neues_erscheinungsdatum is not None:
                sql_parts.append("erscheinungsdatum = %s")
                values.append(neues_erscheinungsdatum)
            if neuer_benutzer_id is not None:
                sql_parts.append("benutzer_id = %s")
                values.append(neuer_benutzer_id)
            else:
                sql_parts.append("benutzer_id = NULL")

            if sql_parts:
                values.append(zeitschrift_id)
                sql_query = "UPDATE zeitschriften SET " + ", ".join(sql_parts) + " WHERE id = %s"
                cursor.execute(sql_query, values)
                conn.commit()
                if cursor.rowcount == 0:
                    return False
                return True
            else:
                return False
        except mysql.connector.Error as err:
            print(f"Fehler beim Aktualisieren der Zeitschrift: {err}")
            return False
        finally:
            cursor.close()
            conn.close()
    return False

def delete_zeitschrift(zeitschrift_id, benutzer_id):
    """
    Löscht eine Zeitschrift komplett aus der Datenbank.
    Gibt True zurück, wenn erfolgreich gelöscht, sonst False.
    """
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True) if conn else None
        try:
            # Zeitschrift-Titel holen
            zeitschrift = None
            if cursor:
                cursor.execute("SELECT titel FROM zeitschriften WHERE id = %s", (zeitschrift_id,))
                zeitschrift = cursor.fetchone()
            if not zeitschrift:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()
                return False  # Keine Zeitschrift gefunden

            # Benutzer holen
            user = User.get_by_id(benutzer_id)
            if not user:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()
                return False  # Kein Benutzer gefunden

            # Zeitschrift löschen
            if cursor:
                cursor.execute("DELETE FROM ausleihen WHERE zeitschrift_id = %s", (zeitschrift_id,))
                cursor.execute("DELETE FROM zeitschriften WHERE id = %s", (zeitschrift_id,))
                if hasattr(cursor, 'rowcount') and cursor.rowcount == 0:
                    if conn:
                        conn.close()
                    return False  # Nichts gelöscht
            else:
                if conn:
                    conn.close()
                return False  # Kein Cursor vorhanden

            # Protokollierung entfernt

            if conn:
                conn.commit()
            if cursor:
                cursor.close()
            if conn:
                conn.close()
            return True

        except mysql.connector.Error as err:
            print(f"Fehler beim Löschen der Zeitschrift: {err}")
            if cursor:
                cursor.close()
            if conn:
                conn.close()
            return False

    return False


def barcode_existiert(barcode):
    """
    Checkt ob barcode bereits in DB vorhanden.
    Gibt True (existiert) oder False (existiert nicht) zurück
    """
    conn = get_db_connection()

    if conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM zeitschriften WHERE barcode = %s', (barcode,))
        zeitschrift = cursor.fetchone()
        cursor.close()
        conn.close()

        if zeitschrift:
            return True
        
    return False

def suche_zeitschriften(titel=None, barcode=None):
    """
    Zeitschriften anhand des Titels oder des Barcodes suchen
    """
    conn = get_db_connection()

    if conn:
        cursor = conn.cursor(dictionary=True)
        query = 'SELECT * FROM zeitschriften WHERE aktiv = 1'
        params = []

        if titel:
            query += ' AND titel LIKE %s'
            params.append(f'%{titel}%')

        if barcode:
            query += ' AND barcode = %s'
            params.append(barcode)

        cursor.execute(query, tuple(params))
        ergebnisse = cursor.fetchall()
        cursor.close()
        conn.close()

        return ergebnisse
    
    return []

def top_ausleihen(limit=10):
    """"
    Gibt die am häufigsten ausgeliehenenen Zeitschriften zurück. Sortiert nach Anzahl der Ausleihen beginnend mit der Größten
    """
    try:
        conn = get_db_connection()

        if conn:
            cursor = conn.cursor(dictionary=True)
            query = 'SELECT zeitschrift_id, COUNT(*) AS anzahl_ausleihen FROM ausleihen GROUP BY zeitschrift_id ORDER BY anzahl_ausleihen DESC LIMIT %s;'
            cursor.execute(query, (limit,))
            ergebnisse = cursor.fetchall()
            cursor.close()
            conn.close()
            return ergebnisse
    except Exception as e:
        return {"error": f"Verbindung zur Datenbank fehlgeschlagen: {str(e)}"}
        
def aktuell_ausgeliehen():
    """
    Gibt eine Liste der aktuell ausgeliehenen Zeitschriften zurück
    """
    try:
        conn = get_db_connection()

        if conn:
            cursor = conn.cursor(dictionary=True)
            query = 'SELECT zeitschrift_id, benutzer_id, ausleihdatum FROM ausleihen WHERE rueckgabedatum IS NULL ORDER BY ausleihdatum;'
            cursor.execute(query)
            ergebnisse = cursor.fetchall()
            cursor.close()
            conn.close()
            return ergebnisse
        else:
            return []
    except Exception as e:
        return {"error": f"Fehler beim Abrufen der aktuellen Ausleihen: {str(e)}"}

def zeitschrift_ausleihen_internal(zeitschrift_id, benutzer_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True) if conn else None

    # Zeitschrift holen
    zeitschrift = None
    if cursor:
        cursor.execute('SELECT titel FROM zeitschriften WHERE id = %s', (zeitschrift_id,))
        zeitschrift = cursor.fetchone()

    # Benutzer holen
    user = User.get_by_id(benutzer_id)

    # Zeitschrift ausleihen
    if cursor:
        cursor.execute('UPDATE zeitschriften SET benutzer_id = %s WHERE id = %s', (benutzer_id, zeitschrift_id))
        cursor.execute('''
            INSERT INTO ausleihen (zeitschrift_id, benutzer_id, ausleihdatum)
            VALUES (%s, %s, NOW())
        ''', (zeitschrift_id, benutzer_id))
    if conn:
        conn.commit()
    # Protokollierung entfernt
    if cursor:
        cursor.close()
    if conn:
        conn.close()

    return jsonify({
        "message": f"{user.firstname if user else ''} {user.name if user else ''} hat '{zeitschrift['titel'] if zeitschrift else ''}' ausgeliehen."
    }), 201


def zeitschrift_rueckgabe_internal(zeitschrift_id, benutzer_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True) if conn else None

    # Zeitschrift holen
    zeitschrift = None
    if cursor:
        cursor.execute('SELECT titel FROM zeitschriften WHERE id = %s', (zeitschrift_id,))
        zeitschrift = cursor.fetchone()

    # Benutzer holen
    user = User.get_by_id(benutzer_id)

    # Rückgabe durchführen
    if cursor:
        cursor.execute('UPDATE zeitschriften SET benutzer_id = NULL WHERE id = %s', (zeitschrift_id,))
        cursor.execute('''
            UPDATE ausleihen
            SET rueckgabedatum = NOW()
            WHERE zeitschrift_id = %s AND benutzer_id = %s AND rueckgabedatum IS NULL
        ''', (zeitschrift_id, benutzer_id))
    if conn:
        conn.commit()
    # Protokollierung entfernt
    if cursor:
        cursor.close()
    if conn:
        conn.close()

    return jsonify({
        "message": f"{user.firstname if user else ''} {user.name if user else ''} hat '{zeitschrift['titel'] if zeitschrift else ''}' zurückgegeben."
    }), 200


def get_zeitschrift_titel(zeitschrift_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True) if conn else None
    zeitschrift = None
    if cursor:
        cursor.execute('SELECT titel FROM zeitschriften WHERE id = %s', (zeitschrift_id,))
        zeitschrift = cursor.fetchone()
        cursor.close()
    if conn:
        conn.close()
    return zeitschrift['titel'] if zeitschrift else ''