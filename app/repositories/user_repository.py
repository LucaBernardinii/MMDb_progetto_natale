# Importiamo la nostra funzione per prendere la connessione
from app.db import get_db
import sqlite3

# Lo schema definisce la tabella 'users' con colonna 'password_hash'

def create_user(username, password_hash, email):
    """Inserisce un nuovo utente (username, email, password_hash)."""
    db = get_db()
    try:
        db.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
            (username, email, password_hash),
        )
        db.commit() # Salviamo le modifiche
        return True
    except sqlite3.IntegrityError:
        # Errore: lo username o l'email esistono già
        return False

def get_user_by_username(username):
    """Cerca un utente per nome."""
    db = get_db()
    user = db.execute(
        "SELECT * FROM users WHERE username = ?", (username,)
    ).fetchone()
    return user

def get_user_by_id(user_id):
    """Cerca un utente per ID."""
    db = get_db()
    user = db.execute(
        "SELECT * FROM users WHERE id = ?", (user_id,)
    ).fetchone()
    return user