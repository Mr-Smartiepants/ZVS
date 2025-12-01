# Datenbankmodell für Exemplare

import mysql.connector
from . import get_db_connection
from datetime import datetime

def add_exemplar(barcode, erscheinungsdatum, ausgabe_heftnummer, zeitschrift_id):
    """ein neues Exemplar hinzufügen."""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                '''
                INSERT INTO exemplare (Barcode, Erscheinungsdatum, AusgabeHeftnummer, Aktiv, ZeitschriftID)
                VALUES (%s, %s, %s, %s, %s)
                ''',
                (barcode, erscheinungsdatum, ausgabe_heftnummer, 1, zeitschrift_id)
            )
            conn.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Fehler beim Hinzufügen des Exemplars: {err}")
            return False
        finally:
            cursor.close()
            conn.close()
    return False

def get_all_aktive_exemplare():
    """Alle aktiven Exemplare mit Titel zurückgeben."""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            '''
            SELECT
                e.ExemplarID,
                e.Barcode,
                e.Erscheinungsdatum,
                e.AusgabeHeftnummer,
                e.Aktiv,
                z.Titel,
                z.ZeitschriftID
            FROM exemplare e
            JOIN zeitschriften z ON e.ZeitschriftID = z.ZeitschriftID
            WHERE e.Aktiv = 1
            '''
        )
        exemplare = cursor.fetchall() if cursor else []
        cursor.close()
        conn.close()
        return exemplare
    return []

def barcode_existiert(barcode):
    """checken ob barcode bereits vorhanden"""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('SELECT ExemplarID FROM exemplare WHERE Barcode = %s', (barcode,))
        exemplar = cursor.fetchone()
        cursor.close()
        conn.close()
        return exemplar is not None
    return False

def get_exemplar_by_barcode(barcode):
    """Exemplar anhand des Barcodes zurückgeben."""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            '''
            SELECT
                e.ExemplarID,
                e.Barcode,
                e.Erscheinungsdatum,
                e.AusgabeHeftnummer,
                z.Titel,
                z.ZeitschriftID
            FROM exemplare e
            JOIN zeitschriften z ON e.ZeitschriftID = z.ZeitschriftID
            WHERE e.Barcode = %s AND e.Aktiv = 1
            ''', (barcode,))
        exemplar = cursor.fetchone()
        cursor.close()
        conn.close()
        return exemplar
    return None

def delete_exemplar(exemplar_id):
    """Exemplar inaktiv setzen (= SoftDelete)."""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('UPDATE exemplare SET Aktiv = 0 WHERE ExemplarID = %s', (exemplar_id,))
            conn.commit()
            return cursor.rowcount > 0
        except mysql.connector.Error as err:
            print(f"Fehler beim Löschen des Exemplars: {err}")
            return False
        finally:
            cursor.close()
            conn.close()
    return False

 