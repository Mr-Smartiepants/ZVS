import bcrypt
from flask import Blueprint, request, redirect, url_for, flash, render_template, session
from flask_login import login_user, logout_user, login_required, current_user
from models.user import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/list_users', methods=['GET'])
@login_required
def list_users():
    # Überprüfen, ob der aktuelle Benutzer ein Admin ist
    if current_user.role != 'admin':
        flash("Zugriff verweigert! Nur Admins dürfen diese Seite aufrufen.", "error")
        return redirect(url_for('index'))

    # Aktion protokollieren
    User.protokolliere_aktion(current_user.id, "hat Benutzerliste aufgerufen")

    # Benutzer aus der Datenbank abrufen
    users_data = User.get_all_users()  # Gibt ein Dictionary mit 'admins' und 'users' zurück
    admins = users_data['admins']
    users = users_data['users']
    # Hole die Daten des aktuell eingeloggten Benutzers
    vorname = current_user.firstname
    name = current_user.name
    
    return render_template(
        'list_users.html',
        admins=admins,
        users=users,
        vorname=vorname,
        name=name
    )

@auth_bp.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    if request.method == 'POST':
        firstname = request.form['firstname']
        name = request.form['name']
        is_admin = 'is_admin' in request.form  # Prüfen, ob die Admin-Checkbox aktiviert ist

        if is_admin:
            result = add_admin(firstname, name, request.form['password'])
            if 'erfolgreich' in str(result):
                User.protokolliere_aktion(current_user.id, f"hat Admin {firstname} {name} hinzugefügt")
            return result
        else:
            result = add_normal_user(firstname, name)
            if 'erfolgreich' in str(result):
                User.protokolliere_aktion(current_user.id, f"hat Benutzer {firstname} {name} hinzugefügt")
            return result

    return render_template('add_user.html')


def add_admin(firstname, name, password):
    if not password:
        flash("Admins benötigen ein Passwort.", "error")
        return redirect(url_for('auth.add_user'))

    if User.get_by_fullname(firstname, name):
        flash('Ein Benutzer mit diesem Vor- und Nachnamen existiert bereits.', 'error')
        return redirect(url_for('auth.add_user'))

    username = generiere_benutzername(firstname, name)
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    User.create_user(username=username, password=hashed_password, name=name, firstname=firstname, role='admin')

    flash(f'Admin {firstname} {name} wurde erfolgreich hinzugefügt.', 'success')
    return redirect(url_for('auth.list_users'))


def add_normal_user(firstname, name):
    if User.get_by_fullname(firstname, name):
        flash('Ein Benutzer mit diesem Vor- und Nachnamen existiert bereits.', 'error')
        return redirect(url_for('auth.add_user'))

    username = generiere_benutzername(firstname, name)

    # Passwort ist None für normale Benutzer
    User.create_user(username=username, password=None, name=name, firstname=firstname, role='user')

    flash(f'Benutzer {firstname} {name} wurde erfolgreich hinzugefügt.', 'success')
    return redirect(url_for('auth.list_users'))

@auth_bp.route('/remove_user', methods=['POST'])
@login_required
def remove_user():
    # Überprüfen, ob der aktuelle Benutzer ein Admin ist
    if current_user.role != 'admin':
        flash("Zugriff verweigert! Nur Admins dürfen Benutzer entfernen.", "error")
        return redirect(url_for('index'))

    # Benutzer-ID aus dem Formular abrufen
    user_id = request.form.get('user_id')

    if not user_id:
        flash("Keine Benutzer-ID angegeben.", "error")
        return redirect(url_for('auth.list_users'))

    user = User.get_by_id(user_id)

    if user:
        # Benutzer aus der Datenbank löschen
        User.delete_user(user_id)
        User.protokolliere_aktion(current_user.id, f"hat Benutzer {user.firstname} {user.name} entfernt")
        flash(f"Benutzer {user.firstname} {user.name} wurde erfolgreich entfernt.", "success")
    else:
        flash("Benutzer nicht gefunden.", "error")

    return redirect(url_for('auth.list_users'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.get_by_username(username)

        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            login_user(user)
            # Nach erfolgreichem Login
            User.protokolliere_aktion(user.id, "hat sich angemeldet")
            return redirect(url_for('admin_dashboard'))
        else:
            # Fehlgeschlagener Loginversuch protokollieren
            if user:
                User.protokolliere_aktion(user.id, "fehlgeschlagener Loginversuch")
            flash('Benutzername oder Passwort falsch.', 'error')

    return render_template('admin_login.html')

def konvertiere_sonderzeichen(text):
    text = text.replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue')
    text = text.replace('Ä', 'Ae').replace('Ö', 'Oe').replace('Ü', 'Ue')
    text = text.replace('ß', 'ss')
    return text

def generiere_benutzername(firstname, name):
    # Konvertiere Umlaute und Sonderzeichen
    name_konvertiert = konvertiere_sonderzeichen(name)
    firstname_konvertiert = konvertiere_sonderzeichen(firstname)
    benutzername = (name_konvertiert + firstname_konvertiert[0]).lower()

    # Überprüfe, ob der Benutzername bereits existiert
    if User.get_by_username(benutzername):
        # Falls der Benutzername existiert, füge den zweiten Buchstaben des Vornamens hinzu
        benutzername = (name_konvertiert + firstname_konvertiert[0:2]).lower()

        # Falls dieser Benutzername auch existiert, füge eine Zahl hinzu
        suffix = 1
        while User.get_by_username(benutzername):
            benutzername = (name_konvertiert + firstname_konvertiert[0:2]).lower() + str(suffix)
            suffix += 1

    return benutzername



@auth_bp.route('/login_user/<int:user_id>', methods=['GET'])
def login_user_route(user_id):
    user = User.get_by_id(user_id)
    if user and user.role == 'user':
        login_user(user)
        session.permanent = True  # Sitzung permanent machen
        # Aktion protokollieren
        User.protokolliere_aktion(user_id, "hat sich als Nutzer eingeloggt")
        flash(f"Willkommen, {user.firstname}! Du wurdest erfolgreich eingeloggt.", "success")
        return redirect(url_for('zeitschriften.scan_page', user_id=user_id))
    else:
        flash("Ungültiger Benutzer oder Zugriff verweigert.", "error")
        return redirect(url_for('auth.login'))


# Ausloggen für angemeldete user
@auth_bp.route('/logout')
@login_required
def logout():
    User.protokolliere_aktion(current_user.id, "hat sich abgemeldet")
    logout_user()
    return redirect(url_for('auth.login'))

@auth_bp.route('/confirm_user/<int:user_id>', methods=['GET', 'POST'])
def confirm_user(user_id):
    user = User.get_by_id(user_id)
    if not user:
        flash("Benutzer nicht gefunden.", "error")
        return redirect(url_for('index'))

    if request.method == 'POST':
        # Benutzer bestätigen und einloggen
        login_user(user)
        User.protokolliere_aktion(user_id, "hat sich bestätigt und eingeloggt")
        flash(f"Willkommen, {user.firstname}! Du wurdest erfolgreich eingeloggt.", "success")
        return redirect(url_for('zeitschriften.scan_page', user_id=user_id))  # Weiterleitung zur Scan-Seite

    return render_template('confirm_user.html', user=user)