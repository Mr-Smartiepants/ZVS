# Datenbankmodell für Zeitschriften

import mysql.connector
from . import get_db_connection


def add_zeitschrift(titel, barcode=None, ausgabe_heftnummer=None, erscheinungsdatum=None, bestand=0):
    """Fügt eine neue Zeitschrift im Katalog hinzu und legt direkt eine Bestandszeile an."""
    try:
        bestand_wert = max(int(bestand or 0), 0)
    except (TypeError, ValueError):
        bestand_wert = 0
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                '''
                INSERT INTO zeitschriften (Titel, barcode, ausgabe_heftnummer, erscheinungsdatum, aktiv)
                VALUES (%s, %s, %s, %s, 1)
                ''',
                (titel, barcode, ausgabe_heftnummer, erscheinungsdatum)
            )
            zeitschrift_id = cursor.lastrowid

            # Bestandszeile anlegen (falls bereits vorhanden, Bestand auffüllen)
            cursor.execute(
                '''
                INSERT INTO exemplare (ZeitschriftID, Bestand, Verfuegbar, Aktiv)
                VALUES (%s, %s, %s, 1)
                ON DUPLICATE KEY UPDATE
                    Bestand = Bestand + VALUES(Bestand),
                    Verfuegbar = Verfuegbar + VALUES(Verfuegbar),
                    Aktiv = 1
                ''',
                (zeitschrift_id, bestand_wert, bestand_wert)
            )

            conn.commit()
            return zeitschrift_id
        except mysql.connector.Error as err:
            print(f"Fehler beim Hinzufügen der Zeitschrift: {err}")
            return False
        finally:
            cursor.close()
            conn.close()
    return False


def barcode_existiert(barcode, exclude_id=None):
    """Prüft, ob der Barcode bereits einer anderen Zeitschrift zugeordnet ist."""
    if not barcode:
        return False
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        if exclude_id:
            cursor.execute('SELECT ZeitschriftID FROM zeitschriften WHERE barcode = %s AND ZeitschriftID != %s', (barcode, exclude_id))
        else:
            cursor.execute('SELECT ZeitschriftID FROM zeitschriften WHERE barcode = %s', (barcode,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row is not None
    return False


def get_all_zeitschriften():
    """Gibt alle aktiven Zeitschriften mit Bestands-Statistik zurück."""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT 
                z.ZeitschriftID AS ZeitschriftID,
                z.Titel AS Titel,
                z.barcode,
                z.ausgabe_heftnummer AS AusgabeHeftnummer,
                z.erscheinungsdatum AS Erscheinungsdatum,
                COALESCE(e.Bestand, 0) AS bestand,
                COALESCE(e.Verfuegbar, 0) AS verfuegbar,
                COALESCE(e.Bestand, 0) - COALESCE(e.Verfuegbar, 0) AS ausgeliehen_count
            FROM zeitschriften z
            LEFT JOIN exemplare e ON z.ZeitschriftID = e.ZeitschriftID AND e.Aktiv = 1
            ORDER BY z.Titel
        ''')
        zeitschriften = cursor.fetchall() if cursor else []
        cursor.close()
        conn.close()
        return zeitschriften
    return []


def get_zeitschrift_by_id(zeitschrift_id):
    """Holt eine Zeitschrift mit zugehörigem Bestand."""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT 
                z.ZeitschriftID AS ZeitschriftID,
                z.Titel AS Titel,
                z.barcode,
                z.ausgabe_heftnummer AS AusgabeHeftnummer,
                z.erscheinungsdatum AS Erscheinungsdatum,
                COALESCE(e.Bestand, 0) AS bestand,
                COALESCE(e.Verfuegbar, 0) AS verfuegbar,
                COALESCE(e.Bestand, 0) - COALESCE(e.Verfuegbar, 0) AS ausgeliehen_count
            FROM zeitschriften z
            LEFT JOIN exemplare e ON z.ZeitschriftID = e.ZeitschriftID AND e.Aktiv = 1
            WHERE z.ZeitschriftID = %s
        ''', (zeitschrift_id,))
        zeitschrift = cursor.fetchone()
        cursor.close()
        conn.close()
        return zeitschrift
    return None


def delete_zeitschrift(zeitschrift_id):
    """Setzt Zeitschrift und Bestand inaktiv (Soft Delete)."""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                'UPDATE exemplare SET Aktiv = 0, Verfuegbar = 0 WHERE ZeitschriftID = %s',
                (zeitschrift_id,)
            )
            try:
                cursor.execute('UPDATE zeitschriften SET aktiv = 0 WHERE ZeitschriftID = %s', (zeitschrift_id,))
            except mysql.connector.Error:
                # Fallback falls Spalte aktiv nicht existiert
                cursor.execute('DELETE FROM zeitschriften WHERE ZeitschriftID = %s', (zeitschrift_id,))
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
    """Gibt die 5 am häufigsten ausgeliehenen Zeitschriften zurück."""
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
            GROUP BY z.ZeitschriftID, z.Titel
            ORDER BY anzahl_ausleihen DESC
            LIMIT 5
        ''')
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
    return []


def verfuegbare_exemplare():
    """Gibt Anzahl verfügbarer Exemplare (Summe über Verfuegbar) zurück."""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT COALESCE(SUM(Verfuegbar), 0) as count
            FROM exemplare e
            JOIN zeitschriften z ON e.ZeitschriftID = z.ZeitschriftID
            WHERE e.Aktiv = 1
        ''')
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row[0] if row else 0
    return 0


def ausgeliehene_exemplare():
    """Gibt Anzahl aktuell ausgeliehener Exemplare zurück."""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT COALESCE(SUM(Bestand - Verfuegbar), 0) as count
            FROM exemplare e
            JOIN zeitschriften z ON e.ZeitschriftID = z.ZeitschriftID
            WHERE e.Aktiv = 1
        ''')
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row[0] if row else 0
    return 0
