import csv
import os
import tempfile
from pathlib import Path
from datetime import datetime

MAPPING_FILE = Path(__file__).parent.parent / 'user_mapping.csv'


def ensure_mapping_file_exists():
    if not MAPPING_FILE.exists():
        MAPPING_FILE.parent.mkdir(parents=True, exist_ok=True)
        # header includes real_name now
        MAPPING_FILE.write_text('username,display_name,role,real_name,created_at\n')
        try:
            os.chmod(MAPPING_FILE, 0o600)
        except Exception:
            pass


def generate_next_username(role: str) -> str:
    """Generate next unique username by checking both DB and CSV."""
    from . import get_db_connection
    
    ensure_mapping_file_exists()
    prefix = 'admin' if role == 'admin' else 'user'
    max_num = 0
    
    # Check CSV
    with open(MAPPING_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            uname = row.get('username', '')
            if uname.startswith(prefix + '#'):
                try:
                    num = int(uname.split('#', 1)[1])
                    if num > max_num:
                        max_num = num
                except Exception:
                    continue
    
    # Check DB for any existing usernames with the pattern
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            # Find max number from benutzer table for this prefix
            cursor.execute(
                f"SELECT MAX(CAST(SUBSTRING(username, {len(prefix) + 2}) AS UNSIGNED)) as max_num "
                f"FROM benutzer WHERE username LIKE %s",
                (f"{prefix}#%",)
            )
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            if result and result.get('max_num'):
                db_max = result.get('max_num')
                if db_max > max_num:
                    max_num = db_max
    except Exception:
        # Silently ignore DB errors; use CSV max as fallback
        pass
    
    return f"{prefix}#{max_num + 1}"


def read_all_mappings():
    ensure_mapping_file_exists()
    rows = []
    with open(MAPPING_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def add_user_mapping(username: str, display_name: str, role: str, real_name: str = ''):
    ensure_mapping_file_exists()
    # append a new row
    with open(MAPPING_FILE, 'a', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['username', 'display_name', 'role', 'real_name', 'created_at'])
        writer.writerow({
            'username': username,
            'display_name': display_name,
            'role': role,
            'real_name': real_name,
            'created_at': datetime.now().isoformat()
        })
    try:
        os.chmod(MAPPING_FILE, 0o600)
    except Exception:
        pass


def get_display_name(username: str):
    ensure_mapping_file_exists()
    with open(MAPPING_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('username') == username:
                return row.get('display_name')
    return None


def get_username_by_display_name(display_name: str) -> str:
    """Look up username by display_name in mapping CSV."""
    ensure_mapping_file_exists()
    with open(MAPPING_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('display_name') == display_name:
                return row.get('username')
    return None


def update_user_mapping(username: str, display_name: str, real_name: str = None):
    ensure_mapping_file_exists()
    rows = []
    updated = False
    with open(MAPPING_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            if r.get('username') == username:
                r['display_name'] = display_name
                if real_name is not None:
                    r['real_name'] = real_name
                updated = True
            rows.append(r)

    # atomic write
    fd, tmp_path = tempfile.mkstemp(dir=str(MAPPING_FILE.parent))
    try:
        with os.fdopen(fd, 'w', encoding='utf-8', newline='') as tmpf:
            writer = csv.DictWriter(tmpf, fieldnames=['username', 'display_name', 'role', 'real_name', 'created_at'])
            writer.writeheader()
            writer.writerows(rows)
        os.replace(tmp_path, str(MAPPING_FILE))
        try:
            os.chmod(MAPPING_FILE, 0o600)
        except Exception:
            pass
    finally:
        if os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except Exception:
                pass

    return updated


def rename_user_mapping(old_username: str, new_username: str, new_role: str = None):
    """Rename a mapping entry from old_username to new_username.

    If the old entry exists it will be updated. If new_role is provided,
    the role field will be updated as well. Returns True if renamed/updated,
    False if the old entry was not found.
    """
    ensure_mapping_file_exists()
    rows = []
    renamed = False
    with open(MAPPING_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            if r.get('username') == old_username:
                r['username'] = new_username
                if new_role is not None:
                    r['role'] = new_role
                r['created_at'] = r.get('created_at') or datetime.now().isoformat()
                renamed = True
            rows.append(r)

    if not renamed:
        return False

    # atomic write
    fd, tmp_path = tempfile.mkstemp(dir=str(MAPPING_FILE.parent))
    try:
        with os.fdopen(fd, 'w', encoding='utf-8', newline='') as tmpf:
            writer = csv.DictWriter(tmpf, fieldnames=['username', 'display_name', 'role', 'real_name', 'created_at'])
            writer.writeheader()
            writer.writerows(rows)
        os.replace(tmp_path, str(MAPPING_FILE))
        try:
            os.chmod(MAPPING_FILE, 0o600)
        except Exception:
            pass
    finally:
        if os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except Exception:
                pass

    return True


def remove_user_mapping(username: str):
    ensure_mapping_file_exists()
    rows = []
    removed = False
    with open(MAPPING_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            if r.get('username') == username:
                removed = True
                continue
            rows.append(r)

    # atomic write
    fd, tmp_path = tempfile.mkstemp(dir=str(MAPPING_FILE.parent))
    try:
        with os.fdopen(fd, 'w', encoding='utf-8', newline='') as tmpf:
            writer = csv.DictWriter(tmpf, fieldnames=['username', 'display_name', 'role', 'created_at'])
            writer.writeheader()
            writer.writerows(rows)
        os.replace(tmp_path, str(MAPPING_FILE))
        try:
            os.chmod(MAPPING_FILE, 0o600)
        except Exception:
            pass
    finally:
        if os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except Exception:
                pass

    return removed
