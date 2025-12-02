# Datenbankmodell für Exemplare (Bestandszeilen je Zeitschrift)

import mysql.connector
from . import get_db_connection


def add_exemplar(zeitschrift_id, anzahl=1):
    """Erhöht den Bestand/Verfügbar-Zähler für eine Zeitschrift oder legt ihn an."""
    try:
        anzahl_int = max(int(anzahl or 0), 0)
    except (TypeError, ValueError):
        anzahl_int = 0

    if anzahl_int <= 0:
        return False

    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            # Bestehenden Bestand laden
            cursor.execute(
                '''
                SELECT ExemplarID, Bestand, Verfuegbar
                FROM exemplare
                WHERE ZeitschriftID = %s AND Aktiv = 1
                ''',
                (zeitschrift_id,)
            )
            row = cursor.fetchone()

            if row:
                cursor.execute(
                '''
                UPDATE exemplare
                SET Bestand = Bestand + %s,
                    Verfuegbar = Verfuegbar + %s
                WHERE ExemplarID = %s
                ''',
                    (anzahl_int, anzahl_int, row['ExemplarID'])
                )
                exemplar_id = row['ExemplarID']
            else:
                cursor.execute(
                    '''
                INSERT INTO exemplare (ZeitschriftID, Bestand, Verfuegbar, Aktiv)
                VALUES (%s, %s, %s, 1)
                ''',
                    (zeitschrift_id, anzahl_int, anzahl_int)
                )
                exemplar_id = cursor.lastrowid

            conn.commit()
            return exemplar_id
        except mysql.connector.Error as err:
            print(f"Fehler beim Hinzufügen/Aktualisieren des Bestands: {err}")
            return False
        finally:
            cursor.close()
            conn.close()
    return False


def get_all_aktive_exemplare():
    """Alle aktiven Bestandszeilen mit Zeitschriftendaten zurückgeben."""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            '''
            SELECT
                e.ExemplarID,
                e.Bestand,
                e.Verfuegbar,
                z.id AS ZeitschriftID,
                z.titel AS Titel,
                z.barcode,
                z.ausgabe_heftnummer,
                z.erscheinungsdatum
            FROM exemplare e
            JOIN zeitschriften z ON e.ZeitschriftID = z.id
            WHERE e.Aktiv = 1
            '''
        )
        exemplare = cursor.fetchall() if cursor else []
        cursor.close()
        conn.close()
        return exemplare
    return []


def barcode_existiert(barcode):
    """Prüft, ob eine Zeitschrift mit dem Barcode existiert."""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM zeitschriften WHERE barcode = %s', (barcode,))
        exemplar = cursor.fetchone()
        cursor.close()
        conn.close()
        return exemplar is not None
    return False


def get_exemplar_by_barcode(barcode):
    """Zeitschrift + Bestand anhand Barcode zurückgeben."""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            '''
            SELECT
                e.ExemplarID,
                e.Bestand,
                e.Verfuegbar,
                z.id AS ZeitschriftID,
                z.titel AS Titel,
                z.barcode,
                z.ausgabe_heftnummer AS AusgabeHeftnummer,
                z.erscheinungsdatum AS Erscheinungsdatum
            FROM zeitschriften z
            LEFT JOIN exemplare e ON e.ZeitschriftID = z.id AND e.Aktiv = 1
            WHERE z.barcode = %s
            ''',
            (barcode,)
        )
        exemplar = cursor.fetchone()
        cursor.close()
        conn.close()
        return exemplar
    return None


def get_exemplar_by_id(exemplar_id):
    """Zeitschrift + Bestand anhand Exemplar-ID zurückgeben."""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            '''
            SELECT
                e.ExemplarID,
                e.Bestand,
                e.Verfuegbar,
                z.id AS ZeitschriftID,
                z.titel AS Titel,
                z.barcode,
                z.ausgabe_heftnummer AS AusgabeHeftnummer,
                z.erscheinungsdatum AS Erscheinungsdatum
            FROM exemplare e
            JOIN zeitschriften z ON e.ZeitschriftID = z.id
            WHERE e.ExemplarID = %s AND e.Aktiv = 1
            ''',
            (exemplar_id,)
        )
        exemplar = cursor.fetchone()
        cursor.close()
        conn.close()
        return exemplar
    return None


def delete_exemplar(exemplar_id):
    """Bestand auf inaktiv setzen und Verfügbarkeit auf 0 setzen."""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                '''
                UPDATE exemplare
                SET Aktiv = 0, Verfuegbar = 0
                WHERE ExemplarID = %s
                ''',
                (exemplar_id,)
            )
            conn.commit()
            return cursor.rowcount > 0
        except mysql.connector.Error as err:
            print(f"Fehler beim Löschen des Exemplars: {err}")
            return False
        finally:
            cursor.close()
            conn.close()
    return False

 
