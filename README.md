# Zeitschriftenverwaltungssystem (ZVS)

## Überblick
Webanwendung zur Verwaltung und Ausleihe von Zeitschriften.
Entwickelt als Abschlussprojekt im Rahmen der Ausbildung zum Fachinformatiker für Anwendungsentwicklung.

Die Anwendung ermöglicht eine einfache Verwaltung von Zeitschriftenexemplaren inklusive Benutzerzuordnung und Statusverwaltung.

---

## Features

- Benutzerverwaltung
- Rollenbasierte Zugriffskontrolle
- Ausleih- und Rückgabelogik
- Suchfunktion
- CRUD-Operationen für Zeitschriften
- Statusverwaltung (aktiv/inaktiv)
- Barcode-Integration

---

## Tech Stack

- Python (Flask)
- MariaDB
- JavaScript
- HTML / CSS
- Git

---

## Projektstruktur & Architektur

Das Projekt ist als klassische Flask-Webanwendung aufgebaut mit klarer Trennung von Routing, Geschäftslogik und Darstellung.

---

### Root-Verzeichnis

```
ZVS/
│
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
├── systemd/

```
---

### Zentrale Dateien

#### `app.py`
Einstiegspunkt der Anwendung.  
Initialisiert Flask, registriert Blueprints und startet die Webanwendung.

#### `config.example.py`
Beispiel-Konfigurationsdatei für Datenbank- und Umgebungsvariablen.  
Produktive Konfiguration erfolgt über `.env`.

#### `requirements.txt`
Liste aller Python-Abhängigkeiten zur Installation via `pip`.

#### `hash.py`
Hilfsfunktionen für sicherheitsrelevante Operationen (z. B. Passwort-Hashing).

---

## Backend-Struktur

### `routes/` – HTTP-Handling & Controller

Enthält die Flask-Routen und verarbeitet eingehende Requests.

```
routes/
├── init.py
├── auth.py
└── zeitschriften.py

```

- **auth.py**  
  Login-Logik, Authentifizierung und Zugriffskontrolle

- **zeitschriften.py**  
  Verarbeitung von CRUD-Operationen, Scan-Workflow, Ausleih- und Rückgabeprozessen

---

### `models/` – Datenzugriff & Geschäftslogik

Kapselt Datenbankoperationen und Fachlogik.

```
models/
├── init.py
├── ausleihe.py
├── exemplar.py
├── statistik.py
├── user.py
├── user_mapping.py
└── zeitschrift.py

```

- **zeitschrift.py** – Verwaltung von Zeitschriften
- **exemplar.py** – Verwaltung einzelner Exemplare
- **ausleihe.py** – Logik für Ausleih- und Rückgabeprozesse
- **user.py** – Benutzer- und Rollenverwaltung
- **user_mapping.py** – Zuordnung/Import-Logik von Benutzern
- **statistik.py** – Auswertungen und Statistiken

---

## Frontend

### `templates/` – Server-side Rendering (Jinja2)

HTML-Templates zur Darstellung der Benutzeroberfläche.

Beispiele:

```
templates/
├── admin_login.html
├── admin_dash.html
├── list_zeitschriften.html
├── edit_zeitschrift.html
├── scan.html
├── confirm_action.html
└── ...

```

Abgedeckte Bereiche:

- Admin-Dashboard
- Benutzerverwaltung
- Zeitschriftenverwaltung
- Scan-Workflow mit Bestätigungslogik
- Rollenbasierte Oberflächen

---

## Utilities & Migration

### `scripts/`

Hilfsskripte für Setup und Datenmigration.

```
scripts/
├── run_sql_file.py
├── export_users_to_mapping.py
└── 002_backfill_display_name.py

```
---

## Deployment

### `systemd/`

```
systemd/
└── zvs.service

```
Systemd-Service-Datei zum Betrieb der Anwendung als Linux-Dienst.

---

## Installation

```bash
git clone …
cd ZVS
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask run
