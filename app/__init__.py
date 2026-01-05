import os
from flask import Flask

def create_app(test_config=None):
    # 1. Creiamo l'istanza di Flask
    # instance_relative_config=True dice a Flask: 
    # "Cerca la cartella 'instance' fuori da 'app', non dentro."
    app = Flask(__name__, instance_relative_config=True)

    # 2. Configurazione di base
    # Qui impostiamo le variabili fondamentali.
    app.config.from_mapping(
        # SECRET_KEY serve a Flask per firmare i dati sicuri (es. sessioni).
        # 'dev' va bene per sviluppare, ma in produzione andrà cambiata.
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        # Diciamo a Flask dove salvare il file del database SQLite
        DATABASE=os.environ.get('DATABASE') or os.path.join(app.instance_path, 'mmdb.sqlite'),
    )

    # Permette di passare una config per i test
    if test_config is not None:
        app.config.update(test_config)

    # Assicuriamoci che la cartella instance esista: SQLite ha bisogno della cartella
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    # --- REGISTRAZIONE BLUEPRINTS ---
    from . import main
    app.register_blueprint(main.bp)
    # --------------------------------
    
    from . import auth
    app.register_blueprint(auth.bp)

    # register new blueprints
    from . import diary, watchlist
    app.register_blueprint(diary.bp)
    app.register_blueprint(watchlist.bp)

    from . import db
    db.init_app(app)
    
    return app