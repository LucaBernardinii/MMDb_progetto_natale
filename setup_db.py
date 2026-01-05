import sqlite3
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_DIR = os.path.join(SCRIPT_DIR, 'instance')
DATABASE_PATH = os.path.join(DATABASE_DIR, 'mmdb.sqlite')
SCHEMA_PATH = os.path.join(SCRIPT_DIR, 'app', 'schema.sql')


def setup():
    if not os.path.exists(DATABASE_DIR):
        os.makedirs(DATABASE_DIR)
        print(f"Cartella '{DATABASE_DIR}' creata.")


    connection = sqlite3.connect(DATABASE_PATH)
    

    try:
        with open(SCHEMA_PATH, 'r') as f:
            connection.executescript(f.read())
        connection.commit()
        print("Ottimo! Tabelle create con successo nel database.")
    except Exception as e:
        print(f"Errore durante la creazione delle tabelle: {e}")
        connection.close()
        return
    
    finally:
        connection.close()

if __name__ == '__main__':
    print("Inizializzazione del database...")
    setup()
    print("Fatto. Ora puoi avviare l'app.")