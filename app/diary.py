from flask import Blueprint, render_template, request, redirect, url_for, flash, g
from app.repositories import diary_repository, movie_repository
from app.auth import login_required

bp = Blueprint('diary', __name__, url_prefix='/diary')

@bp.route('/')
@login_required
def index():
    entries = diary_repository.get_entries_for_user(g.user['id'])
    return render_template('diary/index.html', entries=entries)

@bp.route('/add', methods=('GET', 'POST'))
@login_required
def add():
    if request.method == 'POST':
        title = request.form.get('title')
        watched_on = request.form.get('watched_on')
        rating = request.form.get('rating') or None
        comment = request.form.get('comment') or None

        if not title or not watched_on:
            flash('Titolo e data sono obbligatori.')
        else:
            # find or create movie
            movie = movie_repository.get_by_title(title)
            if movie is None:
                movie = movie_repository.create(title)
            diary_repository.add_entry(g.user['id'], movie['id'], watched_on, rating, comment)
            return redirect(url_for('diary.index'))

    return render_template('diary/add.html')