import bcrypt
from flask import Blueprint, request, redirect, url_for, flash, render_template, session
from flask_login import login_user, logout_user, login_required, current_user
from models.user import User
from models.user_mapping import generate_next_username, add_user_mapping, read_all_mappings, get_display_name, update_user_mapping, remove_user_mapping, get_username_by_display_name
import bcrypt

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

    # Ergänze Anzeigenamen aus der Mapping-CSV (falls vorhanden)
    for u in admins:
        try:
            u['display_name'] = get_display_name(u.get('username')) or ''
        except Exception:
            u['display_name'] = ''
    for u in users:
        try:
            u['display_name'] = get_display_name(u.get('username')) or ''
        except Exception:
            u['display_name'] = ''
    # Hole die Daten des aktuell eingeloggten Benutzers (anonymisiert)
    vorname = current_user.username
    name = ''
    
    return render_template(
        'list_users.html',
        admins=admins,
        users=users,
        vorname=vorname,
        name=name,
        active_page='users'
    )

@auth_bp.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    if request.method == 'POST':
        display_name = request.form.get('display_name')
        is_admin = 'is_admin' in request.form

        role = 'admin' if is_admin else 'user'

        # Generiere anonymen Benutzernamen
        username = generate_next_username(role)

        # Passwort nur für Admins
        password = None
        if is_admin:
            pw = request.form.get('password')
            if not pw:
                flash('Admins benötigen ein Passwort.', 'error')
                return redirect(url_for('auth.add_user'))
            password = bcrypt.hashpw(pw.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        erfolg = User.create_user(username=username, password=password, role=role)
        if erfolg:
            # Mapping speichern (display name getrennt)
            real_name = request.form.get('real_name', '').strip()
            add_user_mapping(username, display_name or '', role, real_name)
            User.protokolliere_aktion(current_user.id, f"hat Benutzer {username} hinzugefügt")
            flash(f'Benutzer {username} wurde erfolgreich hinzugefügt.', 'success')
            return redirect(url_for('auth.list_users'))
        else:
            flash('Fehler beim Erstellen des Benutzers.', 'error')
            return redirect(url_for('auth.add_user'))

    return render_template('add_user.html', active_page='users')


@auth_bp.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    # only admins may edit usernames/roles
    if current_user.role != 'admin':
        flash("Zugriff verweigert! Nur Admins dürfen Benutzer bearbeiten.", "error")
        return redirect(url_for('index'))

    user = User.get_by_id(user_id)
    if not user:
        flash('Benutzer nicht gefunden.', 'error')
        return redirect(url_for('auth.list_users'))

    if request.method == 'POST':
        new_role = request.form.get('role', 'user')
        new_display_name = request.form.get('display_name', '').strip()

        # Update role if changed (username cannot be changed via UI anymore)
        if new_role != user.role:
            success, msg = User.update_username_and_role(user_id, user.username, new_role)
            if not success:
                flash(msg, 'error')
                display_name = get_display_name(user.username) or ''
                return render_template('edit_user.html', user=user, display_name=display_name, active_page='users')
            User.protokolliere_aktion(current_user.id, f"hat Rolle von {user.username} geändert -> {new_role}")
        
        # Update display_name in mapping if changed
        old_display_name = get_display_name(user.username) or ''
        if new_display_name and new_display_name != old_display_name:
            try:
                update_user_mapping(user.username, new_display_name)
                User.protokolliere_aktion(current_user.id, f"hat Anzeigenamen von {user.username} geändert -> {new_display_name}")
                flash('Benutzer erfolgreich aktualisiert.', 'success')
            except Exception as e:
                flash(f'Fehler beim Aktualisieren des Anzeigenamens: {e}', 'error')
        else:
            flash('Benutzer erfolgreich aktualisiert.', 'success')
        
        return redirect(url_for('auth.list_users'))

    # GET: render form
    display_name = get_display_name(user.username) or ''
    return render_template('edit_user.html', user=user, display_name=display_name, active_page='users')

# legacy helpers removed; add_user() handles both admin and normal users now

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
        # Benutzer aus der Datenbank löschen (prüft auf Abhängigkeiten)
        success, msg = User.delete_user(user_id)
        if success:
            User.protokolliere_aktion(current_user.id, f"hat Benutzer {user.username} entfernt")
            flash(msg, "success")
        else:
            User.protokolliere_aktion(current_user.id, f"fehlgeschlagener Löschversuch für Benutzer {user.username}")
            flash(msg, "error")
    else:
        flash("Benutzer nicht gefunden.", "error")

    return redirect(url_for('auth.list_users'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        display_name = request.form.get('display_name', '').strip()
        password = request.form.get('password', '')

        if not display_name:
            flash('Bitte geben Sie Ihren Anzeigenamen ein.', 'error')
            return render_template('admin_login.html')

        # Resolve display_name to username via mapping CSV
        username = get_username_by_display_name(display_name)
        if not username:
            flash('Anzeigename nicht gefunden.', 'error')
            return render_template('admin_login.html')

        user = User.get_by_username(username)

        if user and user.password and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            login_user(user)
            # Nach erfolgreichem Login
            User.protokolliere_aktion(user.id, "hat sich angemeldet")
            return redirect(url_for('admin_dashboard'))
        else:
            # Fehlgeschlagener Loginversuch protokollieren
            if user:
                User.protokolliere_aktion(user.id, "fehlgeschlagener Loginversuch")
            flash('Anzeigename oder Passwort falsch.', 'error')

    return render_template('admin_login.html')

# legacy helpers removed (username generation moved to models.user_mapping)

@auth_bp.route('/login_user/<int:user_id>', methods=['GET'])
def login_user_route(user_id):
    user = User.get_by_id(user_id)
    if user and user.role == 'user':
        login_user(user)
        session.permanent = True  # Sitzung permanent machen
        # Aktion protokollieren
        User.protokolliere_aktion(user_id, "hat sich als Nutzer eingeloggt")
        flash(f"Willkommen, {user.username}! Du wurdest erfolgreich eingeloggt.", "success")
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
        flash(f"Willkommen, {user.username}! Du wurdest erfolgreich eingeloggt.", "success")
        return redirect(url_for('zeitschriften.scan_page', user_id=user_id))  # Weiterleitung zur Scan-Seite

    return render_template('confirm_user.html', user=user)


@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    # Allow user to change their display name; admins may also change their password
    username = current_user.username
    display_name = get_display_name(username) or ''

    if request.method == 'POST':
        new_display = request.form.get('display_name', '').strip()
        if new_display != display_name:
            update_user_mapping(username, new_display)
            User.protokolliere_aktion(current_user.id, 'hat seinen Anzeigenamen geändert')
            flash('Anzeigename aktualisiert.', 'success')
            display_name = new_display

        # password change (admins only)
        if current_user.role == 'admin':
            pw = request.form.get('password')
            pw2 = request.form.get('password_confirm')
            if pw:
                if pw != pw2:
                    flash('Passwörter stimmen nicht überein.', 'error')
                else:
                    hashed = bcrypt.hashpw(pw.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                    User.update_password(current_user.id, hashed)
                    User.protokolliere_aktion(current_user.id, 'hat sein Passwort geändert')
                    flash('Passwort geändert.', 'success')

        return redirect(url_for('auth.profile'))

    return render_template('profile.html', username=username, display_name=display_name, active_page='users')


@auth_bp.route('/admin/mapping', methods=['GET'])
@login_required
def admin_mapping():
    if current_user.role != 'admin':
        flash("Zugriff verweigert! Nur Admins dürfen diese Seite aufrufen.", "error")
        return redirect(url_for('index'))

    mappings = read_all_mappings()
    User.protokolliere_aktion(current_user.id, "hat das User-Mapping angesehen")
    return render_template('admin_mapping.html', mappings=mappings, active_page='users')


@auth_bp.route('/admin/mapping/<username>/edit', methods=['GET', 'POST'])
@login_required
def admin_mapping_edit(username):
    if current_user.role != 'admin':
        flash("Zugriff verweigert!", "error")
        return redirect(url_for('index'))

    if request.method == 'POST':
        display_name = request.form.get('display_name', '')
        update_user_mapping(username, display_name)
        User.protokolliere_aktion(current_user.id, f"hat Mapping für {username} aktualisiert")
        flash('Mapping aktualisiert.', 'success')
        return redirect(url_for('auth.admin_mapping'))

    display_name = get_display_name(username) or ''
    return render_template('admin_mapping_edit.html', username=username, display_name=display_name, active_page='users')


@auth_bp.route('/admin/mapping/<username>/delete', methods=['POST'])
@login_required
def admin_mapping_delete(username):
    if current_user.role != 'admin':
        flash("Zugriff verweigert!", "error")
        return redirect(url_for('index'))

    removed = remove_user_mapping(username)
    if removed:
        User.protokolliere_aktion(current_user.id, f"hat Mapping für {username} entfernt")
        flash('Mapping entfernt.', 'success')
    else:
        flash('Mapping nicht gefunden.', 'warning')
    return redirect(url_for('auth.admin_mapping'))