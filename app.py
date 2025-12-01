# Haupt-Flask-App

from dotenv import load_dotenv
import os
from flask import Flask, render_template, redirect, url_for, flash
from config import Config
from routes.zeitschriften import zeitschriften_bp
from flask_login import LoginManager, current_user, login_required
from models.user import User # User-Model importieren
from routes.auth import auth_bp
from datetime import timedelta
from models.statistik import top_5_ausleihen, benutzer_und_admins_zaehlen, gesamt_ausleihen, aktuell_ausgeliehen, top_5_benutzer, verfuegbare_zeitschriften, ausgeliehene_zeitschriften

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY') # Holt Schlüssel aus Umgebungsvariable



app.config.from_object(Config)

app.register_blueprint(zeitschriften_bp)
app.register_blueprint(auth_bp)

# Flask-Login einrichten
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'  # Setze die Login-Seite


app.permanent_session_lifetime = timedelta(minutes=5)  # Sitzungsdauer auf 5 Minuten begrenzen


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

@app.route('/index')
def index():
    benutzer_liste = User.get_all_users()  # Hole getrennte Listen für Admins und Benutzer
    if current_user.is_authenticated:
        return render_template(
            'index.html',
            firstname=current_user.firstname,
            admins=benutzer_liste['admins'],
            users=benutzer_liste['users']
        )
    else:
        return render_template(
            'index.html',
            firstname=None,
            admins=benutzer_liste['admins'],
            users=benutzer_liste['users']
        )
    
@app.route('/')
def root():
    return redirect(url_for('index'))


@app.route('/admin_login')
def admin_login():
    return render_template('admin_login.html')

@app.route('/admin_dash')
@login_required  # nur für eingeloggte Benutzer
def admin_dashboard():
    if current_user.role != 'admin':  # check ob user admin ist
        flash('Zugriff verweigert! Nur Admins dürfen auf diese Seite zugreifen.')
        return redirect(url_for('index'))  # Weiterleitung zur Startseite.

    stats = {
        'top_ausleihen': top_5_ausleihen(),
        'benutzer': benutzer_und_admins_zaehlen(),
        'gesamt_ausleihen': gesamt_ausleihen(),
        'aktuell_ausgeliehen': aktuell_ausgeliehen(),
        'top_benutzer': top_5_benutzer(),
        'verfuegbar': verfuegbare_zeitschriften(),
        'ausgeliehen': ausgeliehene_zeitschriften(),
    }

    return render_template(
        'admin_dash.html',
        stats=stats,
        vorname=current_user.firstname,
        name=current_user.name,
        active_page='dashboard'
    )

@app.route('/scan')
@login_required
def scan():
    return render_template('scan.html')



app.debug = True

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
    print(f"MYSQL_HOST: {app.config.get('MYSQL_HOST')}")
    print(f"MYSQL_USER: {app.config.get('MYSQL_USER')}")
    app.run(debug=True)

