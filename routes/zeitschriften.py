# Routen für Zeitschriftenverwaltung

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user, login_user

from models.user import User
from models import get_db_connection

from models.zeitschrift import (
    add_zeitschrift,
    get_all_zeitschriften,
    delete_zeitschrift,
    get_zeitschrift_by_id,
    barcode_existiert as zeitschrift_barcode_existiert,
    update_zeitschrift_fields,
)
from models.exemplar import (
    add_exemplar,
    reduce_exemplar,
    get_all_aktive_exemplare,
    get_exemplar_by_barcode,
    get_exemplar_by_id,
    delete_exemplar,
)
from models.ausleihe import ausleihe_erstellen, rueckgabe_erstellen, get_aktuelle_ausleihen, get_ausleihen_by_benutzer
from models.ausleihe import cancel_ausleihe_by_id
from models.statistik import top_5_ausleihen, aktuell_ausgeliehen
from models.user_mapping import get_display_name

# Blueprint für Zeitschriften

zeitschriften_bp = Blueprint('zeitschriften', __name__)


def update_zeitschrift(zeitschrift_id, neuer_titel=None, neuer_benutzer_id=None):
    """Fallback wrapper: versucht, `models.zeitschrift.update_zeitschrift` aufzurufen, sonst No-op."""
    try:
        from models.zeitschrift import update_zeitschrift as _update
        return _update(zeitschrift_id, neuer_titel=neuer_titel, neuer_benutzer_id=neuer_benutzer_id)
    except Exception:
        return False


def suche_zeitschriften(titel=None, barcode=None):
    """Fallback-Suche: versucht models.zeitschrift.suche_zeitschriften, sonst einfache Filter.
    Liefert eine Liste von Treffern zurück (ggf. leer).
    """
    try:
        from models.zeitschrift import suche_zeitschriften as _suche
        return _suche(titel=titel, barcode=barcode)
    except Exception:
        # einfacher Fallback: Suche nach Barcode oder Titel
        results = []
        if barcode:
            ex = get_exemplar_by_barcode(barcode)
            if ex:
                results.append(ex)
            return results
        if titel:
            all_z = get_all_zeitschriften()
            for z in all_z:
                if titel.lower() in z.get('Titel', '').lower():
                    results.append(z)
        return results


@zeitschriften_bp.route('/list_zeitschriften', methods=['GET'])
@login_required
def list_zeitschriften():
    if current_user.role != 'admin':
        flash("Zugriff verweigert! Nur Admins dürfen diese Seite aufrufen.", "error")
        return redirect(url_for('index'))

    # Protokollierung ergänzen
    User.protokolliere_aktion(current_user.id, "hat Zeitschriftenliste aufgerufen")

    zeitschriften = get_all_zeitschriften()  # Holt alle Zeitschriften aus der Datenbank
    vorname = current_user.username
    name = ''
    
    return render_template(
        'list_zeitschriften.html',
        zeitschriften=zeitschriften,
        vorname=vorname,
        name=name,
        active_page='zeitschriften'
    )

@zeitschriften_bp.route('/zeitschriften', methods=['POST', 'GET'])
@login_required
def neue_zeitschrift():
    if current_user.role != 'admin':
        flash("Zugriff verweigert! Nur Admins dürfen Zeitschriften hinzufügen.", "error")
        return redirect(url_for('index'))
    
    if request.method == 'GET':
        barcode_prefill = request.args.get('barcode', '')
        return render_template('neue_zeitschrift.html', active_page='zeitschriften', barcode=barcode_prefill)

    # POST: Neue Zeitschrift erstellen
    titel = request.form.get('titel')
    barcode = request.form.get('barcode', '').strip() or None
    erscheinungsdatum = request.form.get('erscheinungsdatum') or None
    ausgabe_heftnummer = request.form.get('ausgabe_heftnummer')
    bestand_raw = request.form.get('bestand', '0')
    try:
        bestand = max(int(bestand_raw), 0)
    except ValueError:
        bestand = 0
    
    if not titel:
        flash("Titel ist erforderlich.", "error")
        return redirect(url_for('zeitschriften.neue_zeitschrift'))
    
    erfolg = add_zeitschrift(titel, barcode, ausgabe_heftnummer, erscheinungsdatum, bestand)
    if erfolg:
        User.protokolliere_aktion(current_user.id, f"hat Zeitschrift '{titel}' hinzugefügt")
        flash("Zeitschrift wurde erfolgreich hinzugefügt.", "success")
        return redirect(url_for('zeitschriften.list_zeitschriften'))
    
    flash("Konnte Zeitschrift nicht hinzufügen.", "error")
    return redirect(url_for('zeitschriften.neue_zeitschrift'))

# Zeitschrift bearbeiten
@zeitschriften_bp.route('/zeitschriften/<int:zeitschrift_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_zeitschrift(zeitschrift_id):
    if current_user.role != 'admin':
        flash("Zugriff verweigert! Nur Admins dürfen diese Aktion ausführen.", "error")
        return redirect(url_for('index'))

    zeitschrift = get_zeitschrift_by_id(zeitschrift_id)
    if not zeitschrift:
        flash("Zeitschrift nicht gefunden.", "error")
        return redirect(url_for('zeitschriften.list_zeitschriften'))

    if request.method == 'POST':
        titel = request.form.get('titel', '').strip()
        barcode = request.form.get('barcode', '').strip() or None
        erscheinungsdatum = request.form.get('erscheinungsdatum') or None
        ausgabe_heftnummer = request.form.get('ausgabe_heftnummer', '').strip() or None

        if not titel:
            flash("Titel ist erforderlich.", "error")
            return redirect(url_for('zeitschriften.edit_zeitschrift', zeitschrift_id=zeitschrift_id))

        if barcode and zeitschrift_barcode_existiert(barcode, exclude_id=zeitschrift_id):
            flash("Barcode ist bereits einer anderen Zeitschrift zugeordnet.", "error")
            return redirect(url_for('zeitschriften.edit_zeitschrift', zeitschrift_id=zeitschrift_id))

        erfolg = update_zeitschrift_fields(zeitschrift_id, titel, barcode, ausgabe_heftnummer, erscheinungsdatum)
        if erfolg:
            User.protokolliere_aktion(current_user.id, f"hat Zeitschrift {zeitschrift_id} bearbeitet")
            flash("Zeitschrift aktualisiert.", "success")
            return redirect(url_for('zeitschriften.list_zeitschriften'))
        else:
            flash("Konnte Zeitschrift nicht aktualisieren.", "error")

    return render_template('edit_zeitschrift.html', zeitschrift=zeitschrift, active_page='zeitschriften')

    if barcode and zeitschrift_barcode_existiert(barcode):
        flash("Barcode ist bereits vergeben.", "error")
        return redirect(url_for('zeitschriften.neue_zeitschrift'))
    
    erfolg = add_zeitschrift(titel, barcode, ausgabe_heftnummer, erscheinungsdatum, bestand)
    
    if erfolg:
        User.protokolliere_aktion(current_user.id, f"hat Zeitschrift '{titel}' hinzugefügt")
        flash("Zeitschrift erfolgreich hinzugefügt.", "success")
        return redirect(url_for('zeitschriften.list_zeitschriften'))
    else:
        flash("Fehler beim Einfügen der Zeitschrift.", "error")
        return redirect(url_for('zeitschriften.neue_zeitschrift'))
    
@zeitschriften_bp.route('/zeitschriften/<int:id>/delete', methods=['POST', 'GET'])
@login_required
def zeitschrift_inaktiv_setzen(id):
    if current_user.role != 'admin':
        flash("Zugriff verweigert!", "error")
        return redirect(url_for('index'))

    zeitschrift = get_zeitschrift_by_id(id)
    if not zeitschrift:
        flash("Zeitschrift nicht gefunden.", "error")
        return redirect(url_for('zeitschriften.list_zeitschriften'))
    
    # Bei POST löschen
    if request.method == 'POST':
        geloescht = delete_zeitschrift(id)
        if geloescht:
            User.protokolliere_aktion(current_user.id, f"hat Zeitschrift '{zeitschrift['Titel']}' gelöscht")
            flash("Zeitschrift wurde erfolgreich entfernt.", "success")
        else:
            flash("Zeitschrift konnte nicht entfernt werden (ggf. offene Ausleihen).", "error")
        return redirect(url_for('zeitschriften.list_zeitschriften'))
    
    # GET: Bestätigungsseite

    # GET: Bestätigungsseite
    return render_template('confirm_delete_zeitschrift.html', zeitschrift=zeitschrift, active_page='zeitschriften')
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
        cursor.execute('SELECT id, username FROM benutzer')
        benutzer = cursor.fetchall()
        cursor.close()
        conn.close()

        # Anzeigenamen ergänzen (fallback auf username)
        for b in benutzer:
            try:
                b['display_name'] = get_display_name(b.get('username')) or b.get('username')
            except Exception:
                b['display_name'] = b.get('username')

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
    exemplar_id = daten.get('exemplar_id')
    benutzer_id = daten.get('benutzer_id')

    if not exemplar_id or not benutzer_id:
        return jsonify({"error": "Exemplar und Benutzer müssen angegeben werden"}), 400

    erfolg, message = ausleihe_erstellen(exemplar_id, benutzer_id)
    
    if erfolg:
        return jsonify({"message": message}), 201
    else:
        return jsonify({"error": message}), 400


@zeitschriften_bp.route('/zeitschriften/rueckgabe', methods=['POST'])
def zeitschrift_rueckgabe():
    daten = request.get_json()
    exemplar_id = daten.get('exemplar_id') 
    benutzer_id = daten.get('benutzer_id')

    if not exemplar_id:
        return jsonify({"error": "Exemplar muss angegeben werden"}), 400

    erfolg, message = rueckgabe_erstellen(exemplar_id, benutzer_id)
    
    if erfolg:
        return jsonify({"message": message}), 200
    else:
        return jsonify({"error": message}), 400

    
@zeitschriften_bp.route('/berichte/top-ausleihen', methods=['GET'])
def get_top_ausleihen():
    limit = request.args.get('limit', 10, type=int)
    # Verwende vorhandene Statistik-Funktion (Top 5). Ignoriere optionales limit-Argument derzeit.
    ergebnisse = top_5_ausleihen()
    return jsonify(ergebnisse)


@zeitschriften_bp.route('/berichte/aktuell-ausgeliehen', methods=['GET'])
def get_aktuell_ausgeliehen():
    ergebnisse = aktuell_ausgeliehen()

    if isinstance(ergebnisse, dict) and 'error' in ergebnisse:
        return ergebnisse, 500
    
    return jsonify(ergebnisse)


@zeitschriften_bp.route('/admin/ausleihe/<int:ausleihe_id>/cancel', methods=['POST'])
@login_required
def admin_cancel_ausleihe(ausleihe_id):
    if current_user.role != 'admin':
        flash("Zugriff verweigert! Nur Admins dürfen diese Aktion ausführen.", "error")
        return redirect(url_for('admin_dashboard'))

    success = cancel_ausleihe_by_id(ausleihe_id)
    if success:
        User.protokolliere_aktion(current_user.id, f"hat Ausleihe {ausleihe_id} storniert")
        flash('Ausleihe erfolgreich storniert (Rueckgabedatum gesetzt).', 'success')
    else:
        flash('Konnte Ausleihe nicht stornieren (evtl. bereits zurückgegeben).', 'warning')
    return redirect(url_for('admin_dashboard'))


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
    user_id = request.args.get('user_id')
    print(f"Benutzer-ID: {user_id}, Barcode: {barcode}")
    
    # Prüfe ob Exemplar mit diesem Barcode existiert
    exemplar = get_exemplar_by_barcode(barcode)
    
    if exemplar and exemplar.get('ExemplarID'):
        # Weiterleitung zur confirm_action mit exemplar_id
        return redirect(url_for('zeitschriften.confirm_action', exemplar_id=exemplar['ExemplarID'], user_id=user_id))
    else:
        # Exemplar nicht gefunden
        flash("Barcode nicht gefunden oder kein Bestand vorhanden.", "warning")
        return redirect(url_for('zeitschriften.scan_page', user_id=user_id))

@zeitschriften_bp.route('/confirm_action', methods=['POST', 'GET'])
def confirm_action():
    if request.method == 'POST':
        exemplar_id = request.form.get('exemplar_id')
        user_id = request.form.get('user_id')
        action = request.form.get('action')

        try:
            exemplar_id_int = int(exemplar_id)
        except (TypeError, ValueError):
            exemplar_id_int = None

        if exemplar_id_int and user_id:
            user = User.get_by_id(user_id)
            exemplar = get_exemplar_by_id(exemplar_id_int)
            erfolg = False
            message = ""

            if exemplar and user:
                if action == 'rueckgabe':
                    erfolg, message = rueckgabe_erstellen(exemplar_id_int, user_id)
                    if erfolg:
                        ausgabe = exemplar.get('AusgabeHeftnummer') or ''
                        User.protokolliere_aktion(user_id, f"hat '{exemplar['Titel']}' {ausgabe} zurückgegeben")
                elif action == 'ausleihe':
                    erfolg, message = ausleihe_erstellen(exemplar_id_int, user_id)
                    if erfolg:
                        ausgabe = exemplar.get('AusgabeHeftnummer') or ''
                        User.protokolliere_aktion(user_id, f"hat '{exemplar['Titel']}' {ausgabe} ausgeliehen")
                else:
                    message = "Unbekannte Aktion."

            return render_template('aktion_bestaetigt.html', message=message, erfolg=erfolg)
    
    # GET
    exemplar_id = request.args.get('exemplar_id')
    user_id = request.args.get('user_id')
    
    try:
        exemplar_id_int = int(exemplar_id) if exemplar_id else None
    except (TypeError, ValueError):
        exemplar_id_int = None

    exemplar = get_exemplar_by_id(exemplar_id_int) if exemplar_id_int else None
    user = User.get_by_id(user_id) if user_id else None
    try:
        display_name = get_display_name(user.username) if user else ''
    except Exception:
        display_name = user.username if user else ''

    hat_offene_ausleihe = False
    verfuegbar = exemplar.get('Verfuegbar', 0) if exemplar else 0
    if exemplar and user:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True) if conn is not None else None
        if cursor:
            cursor.execute(
                '''
                SELECT COUNT(*) AS count FROM ausleihen
                WHERE ExemplarID = %s AND BenutzerID = %s AND Rueckgabedatum IS NULL
                ''',
                (exemplar['ExemplarID'], user.id)
            )
            result = cursor.fetchone()
            hat_offene_ausleihe = result and result['count'] > 0
            cursor.close()
        if conn:
            conn.close()
    
    return render_template(
        'confirm_action.html',
        zeitschrift=exemplar,
        user=user,
        display_name=display_name,
        hat_offene_ausleihe=hat_offene_ausleihe,
        verfuegbar=verfuegbar
    )

@zeitschriften_bp.route('/rescan/<int:user_id>', methods=['GET'])
def rescan(user_id):
    # Direkt zur Scanner-Seite weiterleiten
    return redirect(url_for('zeitschriften.scan_page', user_id=user_id))

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
    from models.user_mapping import get_display_name
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True) if conn is not None else None
    aktionen = []
    if cursor:
        cursor.execute("""
            SELECT a.id, a.aktion, a.zeitpunkt, b.username
            FROM aktionen a
            LEFT JOIN benutzer b ON a.benutzer_id = b.id
            ORDER BY a.zeitpunkt DESC
        """)
        aktionen = cursor.fetchall()
        
        # Ergänze display_name für jeden Eintrag
        for eintrag in aktionen:
            username = eintrag.get('username')
            if username:
                try:
                    eintrag['display_name'] = get_display_name(username) or username
                except Exception:
                    eintrag['display_name'] = username
            else:
                eintrag['display_name'] = 'unbekannt'
        
        cursor.close()
    if conn:
        conn.close()
    vorname = current_user.username
    name = ''
    return render_template('log.html', aktionen=aktionen, vorname=vorname, name=name, active_page='log')
@zeitschriften_bp.route('/scan_exemplar', methods=['GET', 'POST'])
@login_required
def scan_exemplar():
    if current_user.role != 'admin':
        flash("Zugriff verweigert!", "error")
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        barcode = request.form.get('barcode', '').strip()
        
        if not barcode:
            flash("Bitte scannen Sie einen Barcode.", "error")
            return render_template('scan_exemplar.html', active_page='zeitschriften')
        
        # Prüfen ob Barcode bereits existiert
        if zeitschrift_barcode_existiert(barcode):
            flash(f"Barcode {barcode} existiert bereits.", "error")
            return render_template('scan_exemplar.html', active_page='zeitschriften')
        
        # Weiterleitung zum Zeitschriften-Formular mit Barcode vorausgefüllt
        return redirect(url_for('zeitschriften.neue_zeitschrift', barcode=barcode))
    
    return render_template('scan_exemplar.html', active_page='zeitschriften')


@zeitschriften_bp.route('/exemplare', methods=['POST', 'GET'])
@login_required
def neue_exemplar():
    if current_user.role != 'admin':
        flash("Zugriff verweigert!", "error")
        return redirect(url_for('index'))
    
    if request.method == 'GET':
        # Hole alle Zeitschriften zum Auswählen
        zeitschriften = get_all_zeitschriften()
        return render_template('neue_exemplar.html', zeitschriften=zeitschriften, active_page='zeitschriften')
    # POST: Bestand für Zeitschrift erhöhen
    zeitschrift_id = request.form.get('zeitschrift_id')
    anzahl_raw = request.form.get('anzahl', '0')

    try:
        anzahl = max(int(anzahl_raw), 0)
    except ValueError:
        anzahl = 0
    
    try:
        zeitschrift_id_int = int(zeitschrift_id)
    except (TypeError, ValueError):
        zeitschrift_id_int = None
    
    if not zeitschrift_id_int:
        flash("Bitte wählen Sie eine Zeitschrift aus.", "error")
        return redirect(url_for('zeitschriften.neue_exemplar'))
    
    if anzahl <= 0:
        flash("Bitte geben Sie eine positive Anzahl an.", "error")
        return redirect(url_for('zeitschriften.neue_exemplar'))
    
    erfolg = add_exemplar(zeitschrift_id_int, anzahl)
    
    if erfolg:
        zeitschrift = get_zeitschrift_by_id(zeitschrift_id_int) or {}
        titel_log = zeitschrift.get('Titel') or f"ID {zeitschrift_id}"
        ausgabe_log = zeitschrift.get('AusgabeHeftnummer') or ''
        User.protokolliere_aktion(
            current_user.id,
            f"hat Bestand um {anzahl} erhöht für Zeitschrift '{titel_log}' {ausgabe_log}".strip()
        )
        flash("Bestand erfolgreich angepasst.", "success")
        return redirect(url_for('zeitschriften.list_zeitschriften'))
    else:
        flash("Fehler beim Aktualisieren des Bestands.", "error")
        return redirect(url_for('zeitschriften.neue_exemplar'))


@zeitschriften_bp.route('/exemplare/reduce', methods=['GET', 'POST'])
@login_required
def reduziere_exemplar():
    if current_user.role != 'admin':
        flash("Zugriff verweigert!", "error")
        return redirect(url_for('index'))

    if request.method == 'GET':
        zeitschriften = get_all_zeitschriften()
        return render_template('reduce_exemplar.html', zeitschriften=zeitschriften, active_page='zeitschriften')

    zeitschrift_id = request.form.get('zeitschrift_id')
    anzahl_raw = request.form.get('anzahl', '0')

    try:
        anzahl = max(int(anzahl_raw), 0)
    except ValueError:
        anzahl = 0

    try:
        zeitschrift_id_int = int(zeitschrift_id)
    except (TypeError, ValueError):
        zeitschrift_id_int = None

    if not zeitschrift_id_int:
        flash("Bitte wählen Sie eine Zeitschrift aus.", "error")
        return redirect(url_for('zeitschriften.reduziere_exemplar'))

    if anzahl <= 0:
        flash("Bitte geben Sie eine positive Anzahl an.", "error")
        return redirect(url_for('zeitschriften.reduziere_exemplar'))

    erfolg = reduce_exemplar(zeitschrift_id_int, anzahl)

    if erfolg:
        zeitschrift = get_zeitschrift_by_id(zeitschrift_id_int) or {}
        titel_log = zeitschrift.get('Titel') or f"ID {zeitschrift_id}"
        ausgabe_log = zeitschrift.get('AusgabeHeftnummer') or ''
        User.protokolliere_aktion(
            current_user.id,
            f"hat Bestand um {anzahl} reduziert für Zeitschrift '{titel_log}' {ausgabe_log}".strip()
        )
        flash("Bestand erfolgreich reduziert.", "success")
        return redirect(url_for('zeitschriften.list_zeitschriften'))
    else:
        flash("Fehler beim Reduzieren des Bestands (ggf. nicht genug verfügbare Exemplare).", "error")
        return redirect(url_for('zeitschriften.reduziere_exemplar'))
