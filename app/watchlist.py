from flask import Blueprint, render_template, request, redirect, url_for, flash, g
from app.repositories import watchlist_repository, movie_repository
from app.auth import login_required

bp = Blueprint('watchlist', __name__, url_prefix='/watchlist')

@bp.route('/')
@login_required
def index():
    wl = watchlist_repository.get_or_create_watchlist(g.user['id'])
    items = watchlist_repository.get_items(wl['id'])
    return render_template('watchlist/index.html', items=items)

@bp.route('/add', methods=('GET', 'POST'))
@login_required
def add():
    if request.method == 'POST':
        title = request.form.get('title')
        if not title:
            flash('Titolo richiesto.')
        else:
            movie = movie_repository.get_by_title(title)
            if movie is None:
                movie = movie_repository.create(title)
            wl = watchlist_repository.get_or_create_watchlist(g.user['id'])
            watchlist_repository.add_item(wl['id'], movie['id'])
            return redirect(url_for('watchlist.index'))
    return render_template('watchlist/add.html')

@bp.route('/remove', methods=('POST',))
@login_required
def remove():
    wl = watchlist_repository.get_or_create_watchlist(g.user['id'])
    movie_id = request.form.get('movie_id')
    if movie_id:
        watchlist_repository.remove_item(wl['id'], movie_id)
    return redirect(url_for('watchlist.index'))