import mysql.connector
from . import get_db_connection
from datetime import datetime
from flask import jsonify
from models.user import User
from flask import request, flash, redirect, url_for
from flask_login import current_user, login_required



def top_5_ausleihen():
    conn = get_db_connection()
    if conn is None:
        return []
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT z.titel, COUNT(a.id) AS anzahl
        FROM ausleihen a
        JOIN zeitschriften z ON a.zeitschrift_id = z.id
        GROUP BY z.titel
        ORDER BY anzahl DESC
        LIMIT 5
    """)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def benutzer_und_admins_zaehlen():
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
    conn = get_db_connection()
    if conn is None:
        return []
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT z.titel, z.ausgabe, z.barcode, b.firstname, b.name
        FROM zeitschriften z
        JOIN benutzer b ON z.benutzer_id = b.id
        WHERE z.benutzer_id IS NOT NULL
    """)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def top_5_benutzer():
    conn = get_db_connection()
    if conn is None:
        return []
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT b.firstname, b.name, COUNT(a.id) AS anzahl
        FROM ausleihen a
        JOIN benutzer b ON a.benutzer_id = b.id
        GROUP BY b.id
        ORDER BY anzahl DESC
        LIMIT 5
    """)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def verfuegbare_zeitschriften():
    conn = get_db_connection()
    if conn is None:
        return 0
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM zeitschriften WHERE benutzer_id IS NULL AND aktiv = 1")
    row = cursor.fetchone()
    anzahl = row[0] if row is not None else 0
    cursor.close()
    conn.close()
    return anzahl

def ausgeliehene_zeitschriften():
    conn = get_db_connection()
    if conn is None:
        return 0
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM zeitschriften WHERE benutzer_id IS NOT NULL AND aktiv = 1")
    row = cursor.fetchone()
    anzahl = row[0] if row is not None else 0
    cursor.close()
    conn.close()
    return anzahl