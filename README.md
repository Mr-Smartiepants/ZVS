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

## Architektur

Kurze Beschreibung deiner Struktur:

- `models/` – Datenbankzugriffe
- `routes/` – API- und View-Logik
- `templates/` – HTML
- `static/` – CSS / JS

(Optional: 3–5 Sätze erklären, warum du es so aufgebaut hast.)

---

## Installation

```bash
git clone ...
cd zvs
pip install -r requirements.txt
flask run
