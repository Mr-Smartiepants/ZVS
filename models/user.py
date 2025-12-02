from flask_login import UserMixin
from . import get_db_connection
from .user_mapping import remove_user_mapping, rename_user_mapping


class User(UserMixin):
    def __init__(self, id, username, password, role):
        self.id = id
        self.username = username
        self.password = password
        self.role = role

    @staticmethod
    def get_by_username(username):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, username, password, role FROM benutzer WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            return User(id=user['id'], username=user['username'], password=user['password'], role=user['role'])
        return None

    @staticmethod
    def get_by_id(user_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, username, password, role FROM benutzer WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            return User(id=user['id'], username=user['username'], password=user['password'], role=user['role'])
        return None

    @staticmethod
    def create_user(username, password, role):
        conn = get_db_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO benutzer (username, password, role)
            VALUES (%s, %s, %s)
        ''', (username, password, role))
        conn.commit()
        cursor.close()
        conn.close()
        return True

    @staticmethod
    def delete_user(user_id, benutzer_id=None):
        """Delete a user if safe.

        Returns (success: bool, message: str).
        Protects referential integrity by refusing deletion when dependent
        loan records exist. If no loans exist, related action-log rows are
        removed to allow deletion.
        """
        try:
            conn = get_db_connection()
            if not conn:
                return False, "Datenbankverbindung fehlgeschlagen"

            # check for any *open* loan records referencing this user
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT COUNT(*) AS cnt FROM ausleihen WHERE BenutzerID = %s AND Rueckgabedatum IS NULL", (user_id,))
            row = cursor.fetchone()
            loan_count = row.get('cnt', 0) if row else 0
            cursor.close()

            if loan_count and loan_count > 0:
                conn.close()
                return False, "Der Benutzer hat offene Ausleihen. Rückgaben/Datensätze zuerst entfernen."

            # fetch username before deleting so we can remove mapping
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT username FROM benutzer WHERE id = %s", (user_id,))
            row = cursor.fetchone()
            username = row.get('username') if row else None
            cursor.close()

            # remove related action-log entries so foreign key won't block deletion
            cur = conn.cursor()
            cur.execute("DELETE FROM aktionen WHERE benutzer_id = %s", (user_id,))
            conn.commit()
            cur.close()
            # remove rows from archive loans table if present (historical records)
            try:
                cur = conn.cursor()
                cur.execute("DELETE FROM ausleihen_alt WHERE benutzer_id = %s", (user_id,))
                conn.commit()
                cur.close()
            except Exception:
                # If the table doesn't exist or deletion fails, ignore and continue;
                # we'll surface errors at the final except
                try:
                    cur.close()
                except Exception:
                    pass
            # now safe to delete user
            cur = conn.cursor()
            cur.execute("DELETE FROM benutzer WHERE id = %s", (user_id,))
            conn.commit()
            cur.close()
            conn.close()

            # remove mapping if present
            if username:
                try:
                    remove_user_mapping(username)
                except Exception:
                    pass

            return True, "Benutzer erfolgreich gelöscht"
        except Exception as exc:
            # Ensure connection is closed on error and return message
            try:
                conn.close()
            except Exception:
                pass
            return False, f"Fehler beim Löschen des Benutzers: {exc}"

    @staticmethod
    def get_all_users():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, username, role FROM benutzer")
        users = cursor.fetchall()
        conn.close()
        admins = [user for user in users if user['role'] == 'admin']
        normale_benutzer = [user for user in users if user['role'] == 'user']
        return {'admins': admins, 'users': normale_benutzer}

    @staticmethod
    def protokolliere_aktion(benutzer_id, aktion):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO aktionen (benutzer_id, aktion) VALUES (%s, %s)",
            (benutzer_id, aktion)
        )
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def update_username_and_role(user_id, new_username, new_role):
        """Update a user's username and role.

        Returns (success: bool, message: str).
        Ensures username uniqueness; on success renames mapping entry if present.
        """
        try:
            conn = get_db_connection()
            if not conn:
                return False, "Datenbankverbindung fehlgeschlagen"

            # fetch current username
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT username FROM benutzer WHERE id = %s", (user_id,))
            row = cur.fetchone()
            if not row:
                cur.close()
                conn.close()
                return False, "Benutzer nicht gefunden"
            old_username = row.get('username')
            cur.close()

            # if username changed, ensure uniqueness
            if new_username != old_username:
                cur = conn.cursor(dictionary=True)
                cur.execute("SELECT id FROM benutzer WHERE username = %s", (new_username,))
                exists = cur.fetchone()
                cur.close()
                if exists:
                    conn.close()
                    return False, "Der gewünschte Benutzername ist bereits vergeben."

            # perform update
            cur = conn.cursor()
            cur.execute("UPDATE benutzer SET username = %s, role = %s WHERE id = %s", (new_username, new_role, user_id))
            conn.commit()
            cur.close()
            conn.close()

            # rename mapping if username changed
            if new_username != old_username:
                try:
                    rename_user_mapping(old_username, new_username, new_role)
                except Exception:
                    # non-fatal: mapping update failure should not block user update
                    pass

            return True, "Benutzer erfolgreich aktualisiert"
        except Exception as exc:
            try:
                conn.close()
            except Exception:
                pass
            return False, f"Fehler beim Aktualisieren des Benutzers: {exc}"

