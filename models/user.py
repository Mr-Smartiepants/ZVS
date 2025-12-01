from flask_login import UserMixin
from . import get_db_connection

class User(UserMixin):
    def __init__(self, id, username, password, role, name, firstname):
        self.id = id
        self.username = username
        self.password = password
        self.role = role
        self.firstname = firstname
        self.name = name

    @staticmethod
    def get_by_username(username):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM benutzer WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            return User(id=user['id'], username=user['username'], password=user['password'], role=user['role'], name=user['name'], firstname=user['firstname'])
        
        return None

    @staticmethod
    def get_by_id(user_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM benutzer WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            return User(id=user['id'], username=user['username'], password=user['password'], role=user['role'], name=user['name'], firstname=user['firstname'])
        
        return None
    
    @staticmethod
    def get_by_fullname(firstname, name):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM benutzer WHERE firstname = %s AND name = %s", (firstname, name))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        return user  # Gibt den Benutzer zurück, wenn er gefunden wurde, sonst None
    
    @staticmethod
    def create_user(username, password, role, name, firstname, benutzer_id=None):
        conn = get_db_connection()
        if not conn:
            return False
            
        cursor = conn.cursor()

        # Füge den Benutzer in die Datenbank ein
        cursor.execute('''
            INSERT INTO benutzer (username, password, role, name, firstname)
            VALUES (%s, %s, %s, %s, %s)
        ''', (username, password, role, name, firstname))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        # Protokollierung entfernt
        return True

    @staticmethod
    def delete_user(user_id, benutzer_id=None):
        conn = get_db_connection()
        if not conn:
            return False
            
        cursor = conn.cursor(dictionary=True)
        
        # Benutzer-Informationen für Protokollierung holen
        cursor.execute("SELECT firstname, name, role FROM benutzer WHERE id = %s", (user_id,))
        user_info = cursor.fetchone()
        
        cursor.execute("DELETE FROM benutzer WHERE id = %s", (user_id,))
        conn.commit()
        cursor.close()
        conn.close()
        
        # Protokollierung entfernt
        return True

    @staticmethod
    def get_all_users():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Hole alle Benutzer aus der Datenbank
        cursor.execute("SELECT id, firstname, name, role FROM benutzer")
        users = cursor.fetchall()
        conn.close()

        # Trenne Benutzer nach Rolle
        admins = [user for user in users if user['role'] == 'admin']
        normale_benutzer = [user for user in users if user['role'] == 'user']

        return {'admins': admins, 'users': normale_benutzer}
    
    @staticmethod
    def protokolliere_aktion(benutzer_id, aktion):
        print(f"Protokolliere Aktion: Benutzer-ID={benutzer_id}, Aktion={aktion}")
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO aktionen (benutzer_id, aktion) VALUES (%s, %s)",
            (benutzer_id, aktion)
        )
        conn.commit()
        cursor.close()
        conn.close()
        
