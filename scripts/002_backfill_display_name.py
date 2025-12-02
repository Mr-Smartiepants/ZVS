#!/usr/bin/env python3
"""
Backfill `benutzer.display_name` from `user_mapping.csv` using username as key.

Usage:
  source venv/bin/activate
  python scripts/run_sql_file.py sql/002_add_display_name_to_benutzer.sql
  python scripts/002_backfill_display_name.py

This script uses the application's `get_db_connection()` helper and the
`read_all_mappings()` function to update the DB.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app import app
from models import get_db_connection
from models.user_mapping import read_all_mappings


def backfill():
    mappings = read_all_mappings()
    if not mappings:
        print('Keine Mapping-Einträge gefunden; nichts zu füllen.')
        return 0

    with app.app_context():
        conn = get_db_connection()
        if not conn:
            print('Keine DB-Verbindung. Prüfe app.config.')
            return 2
        cursor = conn.cursor()

        try:
            updated = 0
            for m in mappings:
                username = m.get('username')
                display = m.get('display_name') or ''
                if not username:
                    continue
                cursor.execute('UPDATE benutzer SET display_name = %s WHERE username = %s', (display, username))
                updated += cursor.rowcount
            conn.commit()
            print(f'Backfill fertig. {updated} Zeilen aktualisiert.')
            return 0
        except Exception as e:
            print('Fehler beim Backfill:', e)
            conn.rollback()
            return 3
        finally:
            try:
                cursor.close()
            except Exception:
                pass
            try:
                conn.close()
            except Exception:
                pass


if __name__ == '__main__':
    raise SystemExit(backfill())
