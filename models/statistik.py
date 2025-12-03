# Datenbankmodell für Statistikfunktionen

import mysql.connector
from . import get_db_connection


def top_5_ausleihen():
    """Top 5 am häufigsten ausgeliehenenen Zeitschriften."""
    conn = get_db_connection()
    if conn is None:
        return []
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            z.Titel AS titel,
            z.ausgabe_heftnummer AS ausgabe,
            COUNT(a.AusleiheID) AS anzahl
        FROM ausleihen a
        JOIN exemplare e ON a.ExemplarID = e.ExemplarID
        JOIN zeitschriften z ON e.ZeitschriftID = z.ZeitschriftID
        GROUP BY z.ZeitschriftID
        ORDER BY anzahl DESC
        LIMIT 5
    """)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result


def benutzer_und_admins_zaehlen():
    """Zählt Gesamtbenutzer, Admins und normale Benutzer."""
    conn = get_db_connection()
    if conn is None:
        return {'gesamt': 0, 'admins': 0, 'users': 0}
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) AS gesamt FROM benutzer")
    gesamt_row = cursor.fetchone()
    gesamt = gesamt_row['gesamt'] if gesamt_row is not None else 0
    cursor.execute("SELECT COUNT(*) AS admins FROM benutzer WHERE role = 'admin'")
    admins_row = cursor.fetchone()
    admins = admins_row['admins'] if admins_row is not None else 0
    cursor.close()
    conn.close()
    return {'gesamt': gesamt, 'admins': admins, 'users': gesamt - admins}


def gesamt_ausleihen():
    """Gibt Gesamtzahl aller Ausleihen zurück."""
    conn = get_db_connection()
    if conn is None:
        return 0
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM ausleihen")
    row = cursor.fetchone()
    anzahl = row[0] if row is not None else 0
    cursor.close()
    conn.close()
    return anzahl


def aktuell_ausgeliehen():
    """Gibt Liste der aktuell ausgeliehenenen Exemplare zurück."""
    conn = get_db_connection()
    if conn is None:
        return []
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            a.AusleiheID AS ausleihe_id,
            z.Titel AS titel,
            z.ausgabe_heftnummer AS ausgabe,
            z.barcode AS barcode,
            b.username AS username,
            TIMESTAMPDIFF(DAY, a.Ausleihdatum, NOW()) AS tage
        FROM ausleihen a
        JOIN exemplare e ON a.ExemplarID = e.ExemplarID
        JOIN zeitschriften z ON e.ZeitschriftID = z.ZeitschriftID
        JOIN benutzer b ON a.BenutzerID = b.id
        WHERE a.Rueckgabedatum IS NULL
        ORDER BY tage DESC, a.Ausleihdatum ASC
    """)
    rows = cursor.fetchall()
    # display_name aus Mapping ergänzen
    try:
        from models.user_mapping import get_display_name
        for row in rows:
            try:
                row['display_name'] = get_display_name(row.get('username')) or row.get('username')
            except Exception:
                row['display_name'] = row.get('username')
    except Exception:
        # wenn Mapping nicht erreichbar, einfach username belassen
        for row in rows:
            row['display_name'] = row.get('username')
    cursor.close()
    conn.close()
    return rows


def top_5_benutzer():
    """Top 5 Benutzer mit den meisten Ausleihen."""
    conn = get_db_connection()
    if conn is None:
        return []
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            b.username,
            COUNT(a.AusleiheID) AS anzahl
        FROM ausleihen a
        JOIN benutzer b ON a.BenutzerID = b.id
        GROUP BY b.id
        ORDER BY anzahl DESC
        LIMIT 5
    """)
    rows = cursor.fetchall()
    try:
        from models.user_mapping import get_display_name
        for row in rows:
            try:
                row['display_name'] = get_display_name(row.get('username')) or row.get('username')
            except Exception:
                row['display_name'] = row.get('username')
    except Exception:
        for row in rows:
            row['display_name'] = row.get('username')
    cursor.close()
    conn.close()
    return rows


def verfuegbare_zeitschriften():
    """Gibt Anzahl verfügbarer Exemplare (Summe Verfuegbar) zurück."""
    conn = get_db_connection()
    if conn is None:
        return 0
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COALESCE(SUM(e.Verfuegbar), 0) FROM exemplare e
        JOIN zeitschriften z ON e.ZeitschriftID = z.ZeitschriftID
        WHERE e.Aktiv = 1
    """)
    row = cursor.fetchone()
    anzahl = row[0] if row is not None else 0
    cursor.close()
    conn.close()
    return anzahl


def ausgeliehene_zeitschriften():
    """Zählt aktuell offene Ausleihen (Rueckgabedatum IS NULL)."""
    conn = get_db_connection()
    if conn is None:
        return 0
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM ausleihen WHERE Rueckgabedatum IS NULL")
    row = cursor.fetchone()
    anzahl = row[0] if row else 0
    cursor.close()
    conn.close()
    return anzahl
