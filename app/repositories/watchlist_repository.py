from app.db import get_db

class WatchlistRepository:
    @staticmethod
    def get_or_create_watchlist(user_id):
        db = get_db()
        wl = db.execute('SELECT * FROM watchlists WHERE user_id = ?', (user_id,)).fetchone()
        if wl:
            return wl
        db.execute('INSERT INTO watchlists (user_id) VALUES (?)', (user_id,))
        db.commit()
        return db.execute('SELECT * FROM watchlists WHERE user_id = ?', (user_id,)).fetchone()

    @staticmethod
    def add_item(watchlist_id, movie_id):
        db = get_db()
        try:
            db.execute('INSERT INTO watchlist_items (watchlist_id, movie_id) VALUES (?, ?)', (watchlist_id, movie_id))
            db.commit()
            return True
        except Exception:
            return False

    @staticmethod
    def remove_item(watchlist_id, movie_id):
        db = get_db()
        db.execute('DELETE FROM watchlist_items WHERE watchlist_id = ? AND movie_id = ?', (watchlist_id, movie_id))
        db.commit()

    @staticmethod
    def get_items(watchlist_id):
        db = get_db()
        return db.execute('SELECT wli.*, m.title FROM watchlist_items wli JOIN movies m ON wli.movie_id = m.id WHERE wli.watchlist_id = ?', (watchlist_id,)).fetchall()


watchlist_repository = WatchlistRepository()