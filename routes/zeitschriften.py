# Routen für Zeitschriftenverwaltung

from flask import Blueprint, request, jsonify, render_template, url_for, redirect, flash
from models.zeitschrift import add_zeitschrift, get_all_zeitschriften, update_zeitschrift, delete_zeitschrift, barcode_existiert, suche_zeitschriften, top_ausleihen, aktuell_ausgeliehen, get_db_connection, zeitschrift_ausleihen_internal, zeitschrift_rueckgabe_internal, get_zeitschrift_titel
from flask_login import login_required, current_user, login_user
from models.user import User
# Blueprint für Zeitschriften

zeitschriften_bp = Blueprint('zeitschriften', __name__)


@zeitschriften_bp.route('/list_zeitschriften', methods=['GET'])
@login_required
def list_zeitschriften():
    if current_user.role != 'admin':
        flash("Zugriff verweigert! Nur Admins dürfen diese Seite aufrufen.", "error")
        return redirect(url_for('index'))

    # Protokollierung ergänzen
    User.protokolliere_aktion(current_user.id, "hat Zeitschriftenliste aufgerufen")

    zeitschriften = get_all_zeitschriften()  # Holt alle Zeitschriften aus der Datenbank
    vorname = current_user.firstname
    name = current_user.name
    
    return render_template(
        'list_zeitschriften.html',
        zeitschriften=zeitschriften,
        vorname=vorname,
        name=name
    )

@zeitschriften_bp.route('/zeitschriften', methods=['POST', 'GET'])
@login_required
def neue_zeitschrift():
    if current_user.role != 'admin':
        flash("Zugriff verweigert! Nur Admins dürfen Zeitschriften hinzufügen.", "error")
        return redirect(url_for('index'))

    if request.method == 'GET':
        barcode = request.args.get('barcode', '')  # Barcode aus URL holen
        return render_template('neue_zeitschrift.html', barcode=barcode)

    # POST-Anfragen: Neue Zeitschrift speichern
    titel = request.form.get('titel')
    barcode = request.form.get('barcode')
    ausgabe = request.form.get('ausgabe')
    erscheinungsdatum = request.form.get('erscheinungsdatum')

    if not titel or not barcode or not ausgabe or not erscheinungsdatum:
        flash("Alle Felder sind erforderlich.", "error")
        return redirect(url_for('zeitschriften.neue_zeitschrift', barcode=barcode))

    if barcode_existiert(barcode):
        flash("Der Barcode existiert bereits.", "error")
        return redirect(url_for('zeitschriften.neue_zeitschrift', barcode=barcode))

    erfolg = add_zeitschrift(titel, barcode, ausgabe, erscheinungsdatum)

    if erfolg:
        # Aktion protokollieren
        User.protokolliere_aktion(current_user.id, f"hat Zeitschrift '{titel}' hinzugefügt")
        flash("Zeitschrift erfolgreich hinzugefügt.", "success")
        return redirect(url_for('zeitschriften.list_zeitschriften'))
    else:
        flash("Fehler beim Einfügen der Zeitschrift.", "error")
        return redirect(url_for('zeitschriften.neue_zeitschrift', barcode=barcode))
    
@zeitschriften_bp.route('/zeitschriften/<int:id>/delete', methods=['POST', 'GET'])
@login_required
def zeitschrift_inaktiv_setzen(id):
    if current_user.role != 'admin':
        flash("Zugriff verweigert! Nur Admins dürfen Zeitschriften entfernen.", "error")
        return redirect(url_for('index'))

    conn = get_db_connection()
    if conn is not None:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT titel, benutzer_id FROM zeitschriften WHERE id = %s', (id,))
        zeitschrift = cursor.fetchone()
        cursor.close()
        conn.close()

    if not zeitschrift:
        flash("Zeitschrift nicht gefunden.", "error")
        return redirect(url_for('zeitschriften.list_zeitschriften'))

    # Prüfen, ob ausgeliehen
    if zeitschrift['benutzer_id'] is not None and request.method == 'POST' and not request.form.get('force'):
        ausleiher = User.get_by_id(zeitschrift['benutzer_id'])
        return render_template(
            'confirm_delete_zeitschrift.html',
            zeitschrift=zeitschrift,
            ausleiher=ausleiher
        )

    # Wenn force gesetzt oder nicht ausgeliehen, löschen
    geloescht = delete_zeitschrift(id, current_user.id)
    if geloescht:
        User.protokolliere_aktion(current_user.id, f"hat Zeitschrift '{zeitschrift['titel']}' gelöscht")
        flash("Zeitschrift wurde erfolgreich entfernt.", "success")
    else:
        flash("Zeitschrift konnte nicht entfernt werden.", "error")

    return redirect(url_for('zeitschriften.list_zeitschriften'))


# Route zum aktualisieren einer Zeitschrift

@zeitschriften_bp.route('/zeitschriften/<int:id>', methods=['PUT'])
def zeitschrift_aktualisieren(id):
    daten = request.get_json()
    
    # Extrahiere die neuen Daten aus der Anfrage
    titel = daten.get('titel', None)  # Titel ist optional
    benutzer_id = daten.get('benutzer_id', None)  # benutzer-ID ist ebenfalls optional

    # Überprüfen, ob es etwas zu aktualisieren gibt (entweder Titel oder benutzer-ID)
    if titel is None and benutzer_id is None:
        return jsonify({"error": "Es müssen entweder ein neuer Titel oder eine benutzer-ID übergeben werden"}), 400

    # Versuche, die Zeitschrift zu aktualisieren
    aktualisiert = update_zeitschrift(id, neuer_titel=titel, neuer_benutzer_id=benutzer_id)

    if aktualisiert:
        # Aktion protokollieren
        if benutzer_id:
            User.protokolliere_aktion(benutzer_id, f"hat Zeitschrift '{titel if titel else id}' aktualisiert")
        return jsonify({"message": "Zeitschrift aktualisiert"}), 200
    else:
        return jsonify({"error": "Zeitschrift nicht gefunden oder keine Aktualisierung durchgeführt"}), 404


# Route zum Abrufen aller benutzer
     
@zeitschriften_bp.route('/benutzer', methods=['GET'])
def benutzer_liste():
    conn = get_db_connection()
    if conn is not None:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT id, firstname, name FROM benutzer')
        benutzer = cursor.fetchall()
        cursor.close()
        conn.close()

        # Prüfen, ob der Client JSON erwartet
        if request.headers.get('Accept') == 'application/json':
            return jsonify(benutzer)
        else:
            return render_template('user_selection.html', benutzer_liste=benutzer)

    return jsonify([])  # Falls keine Verbindung zur DB hergestellt werden kann


@zeitschriften_bp.route('/zeitschriften/suchen', methods=['GET'])
def zeitschriften_suchen():

    titel = request.args.get('titel') # Holt Titel aus der Anfrage (Query-Parameter)
    barcode = request.args.get('barcode') # Barcode aus Anfrage holen

    # Suchfunktion aufrufen
    ergebnisse = suche_zeitschriften(titel=titel, barcode=barcode)

    #Suchergebnisse als JSON zurückgeben
    return jsonify(ergebnisse)

@zeitschriften_bp.route('/zeitschriften/ausleihen', methods=['POST'])
def zeitschrift_ausleihen():
    daten = request.get_json()
    zeitschrift_id = daten.get('zeitschrift_id')
    benutzer_id = daten.get('benutzer_id')

    if not zeitschrift_id or not benutzer_id:
        return jsonify({"error": "Zeitschrift und Benutzer müssen angegeben werden"}), 400

    conn = get_db_connection()
    if conn is not None:
        cursor = conn.cursor(dictionary=True)
        # Prüfen, ob die Zeitschrift bereits ausgeliehen ist
        cursor.execute('SELECT titel, benutzer_id FROM zeitschriften WHERE id = %s', (zeitschrift_id,))
        zeitschrift = cursor.fetchone()
        if zeitschrift is not None and zeitschrift.get('benutzer_id') is not None:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
            return jsonify({"error": "Die Zeitschrift ist bereits ausgeliehen."}), 400
        # Zeitschrift ausleihen (benutzer_id aktualisieren)
        cursor.execute('UPDATE zeitschriften SET benutzer_id = %s WHERE id = %s', (benutzer_id, zeitschrift_id))
        conn.commit()
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        # Aktion protokollieren
        if zeitschrift is not None:
            User.protokolliere_aktion(benutzer_id, f"hat Zeitschrift '{zeitschrift['titel']}' ausgeliehen")
        return jsonify({"message": "Ausleihe erfolgreich protokolliert."}), 201
    else:
        return jsonify({"error": "Datenbankverbindung fehlgeschlagen"}), 500

    
@zeitschriften_bp.route('/zeitschriften/rueckgabe', methods=['POST'])
def zeitschrift_rueckgabe():
    daten = request.get_json()
    zeitschrift_id = daten.get('zeitschrift_id')

    if not zeitschrift_id:
        return jsonify({"error": "Zeitschrift muss angegeben werden"}), 400

    conn = get_db_connection()
    if conn is not None:
        cursor = conn.cursor(dictionary=True)
        # Prüfen, ob die Zeitschrift ausgeliehen ist
        cursor.execute('SELECT titel, benutzer_id FROM zeitschriften WHERE id = %s', (zeitschrift_id,))
        zeitschrift = cursor.fetchone()
        if zeitschrift and zeitschrift['benutzer_id'] is None:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
            return jsonify({"error": "Die Zeitschrift ist bereits zurückgegeben."}), 400
        # Zeitschrift zurückgeben (benutzer_id auf NULL setzen)
        cursor.execute('UPDATE zeitschriften SET benutzer_id = NULL WHERE id = %s', (zeitschrift_id,))
        conn.commit()
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        # Aktion protokollieren
        if zeitschrift:
            User.protokolliere_aktion(zeitschrift['benutzer_id'], f"hat Zeitschrift '{zeitschrift['titel']}' zurückgegeben")
        return jsonify({"message": "Rueckgabe erfolgreich protokolliert!"}), 200
    else:
        return jsonify({"error": "Datenbankverbindung fehlgeschlagen"}), 500

    
@zeitschriften_bp.route('/berichte/top-ausleihen', methods=['GET'])
def get_top_ausleihen():
    limit = request.args.get('limit', 10, type=int)
    ergebnisse = top_ausleihen(limit=limit)
    return jsonify(ergebnisse)


@zeitschriften_bp.route('/berichte/aktuell-ausgeliehen', methods=['GET'])
def get_aktuell_ausgeliehen():
    ergebnisse = aktuell_ausgeliehen()

    if isinstance(ergebnisse, dict) and 'error' in ergebnisse:
        return ergebnisse, 500
    
    return jsonify(ergebnisse)


@zeitschriften_bp.route('/scan', methods=['GET', 'POST'])
def scan_page():
    user_id = request.args.get('user_id')
    user_role = None

    if user_id:
        # Benutzer aus der Datenbank holen
        user = User.get_by_id(user_id)
        if user:
            login_user(user)
            user_role = getattr(user, 'role', None)
        else:
            flash("Benutzer nicht gefunden.", "error")
            return redirect(url_for('index'))
    elif current_user.is_authenticated:
        # Kein user_id, aber ein eingeloggter User (z.B. Admin) ist vorhanden
        user_id = current_user.get_id()
        user_role = getattr(current_user, 'role', None)
    else:
        flash("Bitte wählen Sie einen Benutzer aus.", "warning")
        return redirect(url_for('zeitschriften.benutzer_liste'))

    return render_template('scan.html', user_id=user_id, user_role=user_role)


@zeitschriften_bp.route('/process_scan/<string:barcode>', methods=['GET', 'POST'])
@login_required
def process_scan(barcode):
    user_id = request.args.get('user_id')  # Benutzer-ID aus den Query-Parametern holen
    print(f"Benutzer-ID: {user_id}, Barcode: {barcode}")
    
    # Prüfen, ob der Barcode einer Zeitschrift entspricht
    ergebnisse = suche_zeitschriften(barcode=barcode)
    
    if ergebnisse:  # Prüfen, ob die Liste nicht leer ist
        zeitschrift = ergebnisse[0]  # Das erste Ergebnis nehmen
        
        # Weiterleitung zur confirm_action-Route mit Benutzer-ID und Zeitschrift-ID
        return redirect(url_for('zeitschriften.confirm_action', zeitschrift_id=zeitschrift['id'], user_id=user_id))
    
    else:
        # Zeitschrift existiert nicht → Fehlermeldung anzeigen
        flash("Barcode nicht gefunden. Bitte wenden Sie sich an einen Administrator.", "warning")
        return redirect(url_for('zeitschriften.scan_page', user_id=user_id))

@zeitschriften_bp.route('/confirm_action', methods=['POST', 'GET'])
def confirm_action():
    if request.method == 'POST':
        zeitschrift_id = request.form.get('zeitschrift_id')
        user_id = request.form.get('user_id')
        action = request.form.get('action')

        if action == 'confirm':
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True) if conn is not None else None
            zeitschrift = None
            if cursor:
                cursor.execute('SELECT * FROM zeitschriften WHERE id = %s', (zeitschrift_id,))
                zeitschrift = cursor.fetchone()
                cursor.close()
            if conn:
                conn.close()

            user = User.get_by_id(user_id)
            erfolg = False
            message = ""
            if zeitschrift and user:
                if zeitschrift['benutzer_id'] is None:
                    erfolg = zeitschrift_ausleihen_internal(zeitschrift_id, user_id)
                    message = f"{user.firstname} {user.name} hat '{zeitschrift['titel']}' ausgeliehen."
                    # Protokollierung Ausleihe
                    if erfolg:
                        User.protokolliere_aktion(user_id, f"hat Zeitschrift '{zeitschrift['titel']}' ausgeliehen")
                elif str(zeitschrift['benutzer_id']) == str(user_id):
                    erfolg = zeitschrift_rueckgabe_internal(zeitschrift_id, user_id)
                    message = f"{user.firstname} {user.name} hat '{zeitschrift['titel']}' zurückgegeben."
                    # Protokollierung Rückgabe
                    if erfolg:
                        User.protokolliere_aktion(user_id, f"hat Zeitschrift '{zeitschrift['titel']}' zurückgegeben")
                else:
                    ausleiher = User.get_by_id(zeitschrift['benutzer_id']) if zeitschrift['benutzer_id'] else None
                    if ausleiher:
                        message = f"'{zeitschrift['titel']}' ist aktuell ausgeliehen von {ausleiher.firstname} {ausleiher.name}."
                    else:
                        message = f"'{zeitschrift['titel']}' ist aktuell ausgeliehen."
                    erfolg = False
            elif not zeitschrift:
                message = "Zeitschrift nicht gefunden."
                erfolg = False
            elif not user:
                message = "Benutzer nicht gefunden."
                erfolg = False

            return render_template('aktion_bestaetigt.html', message=message, erfolg=erfolg)
        
    # GET-Request: Zeige Bestätigungsseite an
    zeitschrift_id = request.args.get('zeitschrift_id')
    user_id = request.args.get('user_id')
    # Hole Zeitschrift und User für die Anzeige
    zeitschrift = None
    user = None
    if zeitschrift_id:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True) if conn is not None else None
        if cursor:
            cursor.execute('SELECT * FROM zeitschriften WHERE id = %s', (zeitschrift_id,))
            zeitschrift = cursor.fetchone()
            cursor.close()
        if conn:
            conn.close()
    if user_id:
        user = User.get_by_id(user_id)
    return render_template('confirm_action.html', zeitschrift=zeitschrift, user=user)

@zeitschriften_bp.route('/rescan/<int:user_id>', methods=['GET'])
def rescan(user_id):
    # Direkt zur Scanner-Seite weiterleiten
    return redirect(f'/scan/{user_id}')

@zeitschriften_bp.route('/confirm_barcode', methods=['GET', 'POST'])
def confirm_barcode():
    barcode = request.args.get('barcode')
    user_id = request.args.get('user_id')

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'confirm':
            # Weiterleitung zur Seite für neue Zeitschrift mit dem Barcode
            return redirect(url_for('zeitschriften.neue_zeitschrift', barcode=barcode, user_id=user_id))
        elif action == 'rescan':
            # Zurück zur Scan-Seite
            return redirect(url_for('zeitschriften.scan_page', user_id=user_id))
        elif action == 'cancel':
            # Zurück zur Benutzer-Auswahl
            return redirect(url_for('zeitschriften.benutzer_liste'))

    return render_template('confirm_barcode.html', barcode=barcode, user_id=user_id)    

@zeitschriften_bp.route('/log')
@login_required
def aktionen_dashboard():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True) if conn is not None else None
    aktionen = []
    if cursor:
        cursor.execute("""
            SELECT a.id, a.aktion, a.zeitpunkt, b.firstname, b.name
            FROM aktionen a
            LEFT JOIN benutzer b ON a.benutzer_id = b.id
            ORDER BY a.zeitpunkt DESC
        """)
        aktionen = cursor.fetchall()
        cursor.close()
    if conn:
        conn.close()
    vorname = current_user.firstname
    name = current_user.name
    return render_template('log.html', aktionen=aktionen, vorname=vorname, name=name)

