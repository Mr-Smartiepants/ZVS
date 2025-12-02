# Datenbankmodell f+r Ausleihen

import mysql.connector
from . import get_db_connection


def ausleihe_erstellen(exemplar_id, benutzer_id):
    """Neue Ausleihe erstellen und Bestand herunterzählen."""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            # Verfügbarkeit prüfen
            cursor.execute(
                '''
                SELECT Verfuegbar FROM exemplare
                WHERE ExemplarID = %s AND Aktiv = 1
                ''',
                (exemplar_id,)
            )
            row = cursor.fetchone()
            if not row:
                return False, "Bestand nicht gefunden oder inaktiv."
            if row['Verfuegbar'] < 1:
                return False, "Kein Exemplar verfügbar."

            # Verfügbarkeit reduzieren
            cursor.execute(
                '''
                UPDATE exemplare
                SET Verfuegbar = Verfuegbar - 1
                WHERE ExemplarID = %s AND Verfuegbar > 0
                ''',
                (exemplar_id,)
            )
            if cursor.rowcount == 0:
                conn.rollback()
                return False, "Kein Bestand verfügbar."

            # Ausleihe erfassen
            cursor.execute(
                '''
                INSERT INTO ausleihen (ExemplarID, BenutzerID, Ausleihdatum)
                VALUES (%s, %s, NOW())
                ''',
                (exemplar_id, benutzer_id)
            )
            conn.commit()
            return True, "Ausleihe erfolgreich."
        except mysql.connector.Error as err:
            print(f"Fehler beim Erstellen der Ausleihe: {err}")
            conn.rollback()
            return False, str(err)
        finally:
            cursor.close()
            conn.close()
    return False, "Datenbankverbindung fehlgeschlagen."


def rueckgabe_erstellen(exemplar_id, benutzer_id):
    """Rückgabe registrieren und Verfügbarkeit erhöhen."""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                '''
                UPDATE ausleihen
                SET Rueckgabedatum = NOW()
                WHERE ExemplarID = %s AND BenutzerID = %s AND Rueckgabedatum IS NULL
                ORDER BY Ausleihdatum ASC
                LIMIT 1
                ''',
                (exemplar_id, benutzer_id)
            )
            if cursor.rowcount > 0:
                cursor.execute(
                    '''
                    UPDATE exemplare
                    SET Verfuegbar = Verfuegbar + 1
                    WHERE ExemplarID = %s
                    ''',
                    (exemplar_id,)
                )
                conn.commit()
                return True, "Rückgabe erfolgreich."
            else:
                conn.rollback()
                return False, "Keine offene Ausleihe gefunden."
        except mysql.connector.Error as err:
            print(f"Fehler bei der Rückgabe: {err}")
            conn.rollback()
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
                a.AusleiheID AS ausleihe_id,
                z.barcode AS barcode,
                z.Titel AS titel,
                z.ausgabe_heftnummer AS ausgabe,
                b.username AS username,
                a.Ausleihdatum AS ausleihdatum
            FROM ausleihen a
            JOIN exemplare e ON a.ExemplarID = e.ExemplarID
            JOIN zeitschriften z ON e.ZeitschriftID = z.ZeitschriftID
            JOIN benutzer b ON a.BenutzerID = b.id
            WHERE a.Rueckgabedatum IS NULL
            ORDER BY a.Ausleihdatum DESC
            '''
        )
        ausleihen = cursor.fetchall()
        cursor.close()
        conn.close()
        return ausleihen
    return []


def cancel_ausleihe_by_id(ausleihe_id):
    """Markiert eine Ausleihe als zurückgegeben (setzt Rueckgabedatum = NOW()).

    Returns True if a row was updated, False otherwise.
    """
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            # Exemplar für spätere Bestandserhöhung holen
            cursor.execute('SELECT ExemplarID FROM ausleihen WHERE AusleiheID = %s', (ausleihe_id,))
            row = cursor.fetchone()
            exemplar_id = row['ExemplarID'] if row else None

            cursor.execute(
                '''
                UPDATE ausleihen
                SET Rueckgabedatum = NOW()
                WHERE AusleiheID = %s AND Rueckgabedatum IS NULL
                ''', (ausleihe_id,)
            )
            updated = cursor.rowcount > 0
            if updated and exemplar_id:
                cursor.execute(
                    '''
                    UPDATE exemplare
                    SET Verfuegbar = Verfuegbar + 1
                    WHERE ExemplarID = %s
                    ''',
                    (exemplar_id,)
                )
            conn.commit()
            return updated
        except Exception as err:
            print(f"Fehler beim Cancelling der Ausleihe: {err}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()
    return False


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
                z.ausgabe_heftnummer AS AusgabeHeftnummer,
                a.Ausleihdatum,
                a.Rueckgabedatum
            FROM ausleihen a
            JOIN exemplare e ON a.ExemplarID = e.ExemplarID
            JOIN zeitschriften z ON e.ZeitschriftID = z.ZeitschriftID
            WHERE a.BenutzerID = %s
            ORDER BY a.Ausleihdatum DESC 
            ''', (benutzer_id,))
        ausleihen = cursor.fetchall()
        cursor.close()
        conn.close()
        return ausleihen
    return []
