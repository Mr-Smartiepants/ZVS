#!/usr/bin/env python3
"""
Run a .sql file against the application's configured MySQL database
using the existing `models.get_db_connection()` helper (no mysql CLI needed).

Usage:
  source venv/bin/activate
  python scripts/run_sql_file.py sql/001_export_and_drop_name_columns.sql

This will execute the statements in the SQL file. Use with caution — ensure
you have a backup before running destructive commands.
"""
import sys
from pathlib import Path

# ensure project root is importable
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app import app
from models import get_db_connection


def run_sql_file(path: Path):
    sql = path.read_text(encoding='utf-8')
    # Use the Flask application context so get_db_connection() can access app.config
    with app.app_context():
        conn = get_db_connection()
        if not conn:
            print('Keine DB-Verbindung. Prüfe app.config und deine Netzwerkzugänglichkeit zur DB.')
            return 2
        cursor = conn.cursor()
    try:
        # execute as multi-statement
        for result in cursor.execute(sql, multi=True):
            # result is a MySQLCursor; fetch to ensure execution
            try:
                _ = result.fetchall()
            except Exception:
                pass
        conn.commit()
        print('SQL-Datei erfolgreich ausgeführt.')
        return 0
    except Exception as e:
        print('Fehler beim Ausführen der SQL-Datei:', e)
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


def main():
    if len(sys.argv) < 2:
        print('Usage: python scripts/run_sql_file.py path/to/file.sql')
        return 1
    path = Path(sys.argv[1])
    if not path.exists():
        print('Datei nicht gefunden:', path)
        return 1
    return run_sql_file(path)


if __name__ == '__main__':
    raise SystemExit(main())
