import sqlite3
import os
import click
from flask import current_app, g

def get_db():
    """Restituisce la connessione al database per la richiesta corrente."""
    # 'g' è uno zaino temporaneo di Flask. 
    # Se la connessione c'è già, la riusiamo. Se no, la creiamo.
    if 'db' not in g:
        db_path = current_app.config.get('DATABASE')
        try:
            g.db = sqlite3.connect(db_path)
        except sqlite3.OperationalError as e:
            raise RuntimeError(f"Impossibile aprire il file del database '{db_path}': {e}") from e
        # Questa riga serve per poter chiamare le colonne per nome (user['username'])
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    """Chiude la connessione alla fine della richiesta."""
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    """Crea le tabelle eseguendo lo schema SQL (app/schema.sql)."""
    db = get_db()
    schema_path = os.path.join(current_app.root_path, 'schema.sql')
    with open(schema_path, 'r', encoding='utf8') as f:
        db.executescript(f.read())


@click.command('init-db')
def init_db_command():
    """Command-line helper to initialize the database."""
    init_db()
    click.echo('Database inizializzato.')


def init_app(app):
    """Registra la funzione di chiusura automatica e i comandi CLI."""
    # Dice a Flask: "Quando hai finito di caricare la pagina, chiudi sempre il DB"
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)