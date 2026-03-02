# Zeitschriftenverwaltungssystem (ZVS)

## Überblick

Webanwendung zur Verwaltung und Ausleihe von Zeitschriften.  
Entwickelt als Abschlussprojekt im Rahmen der Ausbildung zum Fachinformatiker für Anwendungsentwicklung.

Die Anwendung ermöglicht die Verwaltung von Zeitschriften und einzelnen Exemplaren inklusive Benutzerzuordnung, Rollensteuerung und Statusverwaltung.

---

## Features

- Benutzerverwaltung
- Rollenbasierte Zugriffskontrolle
- Ausleih- und Rückgabelogik
- Suchfunktion
- CRUD-Operationen für Zeitschriften
- Statusverwaltung (aktiv/inaktiv)
- Barcode-Integration
- Statistikfunktionen

---

## Tech Stack

- Python (Flask)
- MariaDB
- JavaScript
- HTML / CSS (Jinja2 Templates)
- Git

---

## Projektstruktur & Architektur

Das Projekt ist als klassische Flask-Webanwendung aufgebaut mit klarer Trennung von Routing (Controller), Geschäftslogik (Model) und Darstellung (Templates).

---

### Root-Verzeichnis

~~~bash
ZVS/
├── app.py
├── config.example.py
├── requirements.txt
├── start_all.sh
├── hash.py
├── .gitignore
│
├── models/
├── routes/
├── templates/
├── scripts/
└── systemd/
~~~

---

## Zentrale Dateien

### `app.py`
Einstiegspunkt der Anwendung.  
Initialisiert Flask, registriert Blueprints und startet die Webanwendung.

### `config.example.py`
Beispiel-Konfigurationsdatei für Datenbank- und Umgebungsvariablen.  
Produktive Konfiguration erfolgt über `.env`.

### `requirements.txt`
Liste aller Python-Abhängigkeiten zur Installation via `pip`.

### `hash.py`
Hilfsfunktionen für sicherheitsrelevante Operationen (z. B. Passwort-Hashing).

---

## Backend-Struktur

### `routes/` – HTTP-Handling & Controller

~~~bash
routes/
├── __init__.py
├── auth.py
└── zeitschriften.py
~~~

- **auth.py** – Login-Logik, Authentifizierung und Zugriffskontrolle  
- **zeitschriften.py** – CRUD-Operationen, Scan-Workflow, Ausleih- und Rückgabeprozesse  

---

### `models/` – Datenzugriff & Geschäftslogik

~~~bash
models/
├── __init__.py
├── ausleihe.py
├── exemplar.py
├── statistik.py
├── user.py
├── user_mapping.py
└── zeitschrift.py
~~~

- **zeitschrift.py** – Verwaltung von Zeitschriften  
- **exemplar.py** – Verwaltung einzelner Exemplare  
- **ausleihe.py** – Logik für Ausleih- und Rückgabeprozesse  
- **user.py** – Benutzer- und Rollenverwaltung  
- **user_mapping.py** – Import-/Mapping-Logik  
- **statistik.py** – Auswertungen und Statistiken  

---

## Frontend

### `templates/` – Server-Side Rendering (Jinja2)

~~~bash
templates/
├── admin_login.html
├── admin_dash.html
├── list_zeitschriften.html
├── edit_zeitschrift.html
├── scan.html
├── confirm_action.html
└── ...
~~~

Abgedeckte Bereiche:

- Admin-Dashboard
- Benutzerverwaltung
- Zeitschriftenverwaltung
- Scan-Workflow mit Bestätigungslogik
- Rollenbasierte Oberflächen

---

## Utilities & Migration

### `scripts/`

~~~bash
scripts/
├── run_sql_file.py
├── export_users_to_mapping.py
└── 002_backfill_display_name.py
~~~

Hilfsskripte für Setup und Datenmigration.

---

## Deployment

### `systemd/`

~~~bash
systemd/
└── zvs.service
~~~

Systemd-Service-Datei zum Betrieb der Anwendung als Linux-Dienst.

---

## Installation

~~~bash
git clone <repository-url>
cd ZVS
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask run
~~~

Hinweis: Datenbank-Konfiguration erfolgt über `.env` basierend auf `config.example.py`.

---

## Lernschwerpunkte & technische Herausforderungen

- Umsetzung einer rollenbasierten Zugriffskontrolle
- Entwicklung einer konsistenten Ausleih- und Rückgabelogik
- Trennung von Geschäftslogik und Präsentation
- Strukturierte Datenbankmodellierung für Zeitschriften und Exemplare
- Implementierung eines Scan-Workflows mit Bestätigungslogik
- Wartbare Projektstruktur mit klarer Modultrennung
