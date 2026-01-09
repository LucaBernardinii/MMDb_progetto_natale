from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
# werkzeug.security ci offre strumenti professionali per la crittografia
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from app.repositories import user_repository

# url_prefix='/auth' significa che tutte le route qui inizieranno con /auth
bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.before_app_request
def load_logged_in_user():
    """
    Questa funzione viene eseguita AUTOMATICAMENTE prima di ogni richiesta.
    Serve a caricare l'utente dal DB e renderlo disponibile in tutto il sito.
    """
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        # Carichiamo l'utente e lo mettiamo in g.user
        # Ora g.user sarà disponibile anche nei template HTML!
        g.user = user_repository.get_user_by_id(user_id)

@bp.route('/register', methods=('GET', 'POST'))
def register():
    # CASO 2: POST (L'utente ha inviato i dati)
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        error = None

        if not username:
            error = 'Username obbligatorio.'
        elif not email:
            error = 'Email obbligatoria.'
        elif not password:
            error = 'Password obbligatoria.'

        if error is None:
            # Hashiamo la password (MAI salvarla in chiaro!)
            hashed_pwd = generate_password_hash(password)
            
            # Chiamiamo il Repository
            success = user_repository.create_user(username, hashed_pwd, email)
            
            if success:
                return redirect(url_for('auth.login'))
            else:
                error = 'Username o email già registrati.'

        flash(error)

    # CASO 1: GET (Mostriamo il form)
    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        
        # 1. Cerchiamo l'utente nel DB
        user = user_repository.get_user_by_username(username)

        if user is None:
            error = 'Username non corretto.'
        # 2. Verifichiamo la password
        elif not check_password_hash(user['password_hash'], password):
            error = 'Password non corretta.'

        if error is None:
            # 3. GESTIONE SESSIONE (Mettiamo il "braccialetto")
            # Puliamo eventuali vecchie sessioni
            session.clear()
            # Salviamo l'ID dell'utente nel cookie di sessione
            session['user_id'] = user['id']
            
            # Ora il browser ricorderà chi siamo!
            return redirect(url_for('main.index'))

        flash(error)

    return render_template('auth/login.html')

def login_required(view):
    """Decorator semplice per proteggere le rotte che richiedono login."""
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view


@bp.route('/logout')
def logout():
    # Per uscire, "tagliamo il braccialetto"
    session.clear()
    return redirect(url_for('main.index'))