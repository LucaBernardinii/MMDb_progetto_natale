from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from app.repositories import diary_repository, watchlist_repository

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    # Mostra la dashboard
    stats = {}

    if g.user:
        uid = g.user['id']
        diary = diary_repository.get_entries_for_user(uid)
        wl = watchlist_repository.get_or_create_watchlist(uid)
        wl_items = watchlist_repository.get_items(wl['id']) if wl else []
        stats['diary_count'] = len(diary)
        stats['watchlist_count'] = len(wl_items)

    return render_template('index.html', stats=stats)

@bp.route('/about')
def about():
    return render_template('about.html')
