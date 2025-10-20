import sqlite3
import hashlib

class Autentificare:
    def __init__(self, db_nume="utilizatori.db"):
        self.conn = sqlite3.connect(db_nume)
        self.cursor = self.conn.cursor()
        self.creeaza_tabel()

    def creeaza_tabel(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS utilizatori (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                parola TEXT NOT NULL,
                rol TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def hash_parola(self, parola):
        return hashlib.sha256(parola.encode()).hexdigest()

    def inregistreaza_utilizator(self, username, parola, rol):
        try:
            parola_hash = self.hash_parola(parola)
            self.cursor.execute('''
                INSERT INTO utilizatori (username, parola, rol)
                VALUES (?, ?, ?)
            ''', (username, parola_hash, rol))
            self.conn.commit()
            print("✅ Utilizator înregistrat cu succes!")
        except sqlite3.IntegrityError:
            print("⚠️ Acest nume de utilizator există deja.")

    def autentifica_utilizator(self, username, parola):
        parola_hash = self.hash_parola(parola)
        self.cursor.execute('''
            SELECT rol FROM utilizatori
            WHERE username = ? AND parola = ?
        ''', (username, parola_hash))
        rezultat = self.cursor.fetchone()
        if rezultat:
            return rezultat[0]  # rolul
        return None
