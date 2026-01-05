from app.db import get_db

class DiaryRepository:
    @staticmethod
    def add_entry(user_id, movie_id, watched_on, rating=None, comment=None):
        db = get_db()
        db.execute(
            'INSERT INTO diary_entries (user_id, movie_id, watched_on, rating, comment) VALUES (?, ?, ?, ?, ?)',
            (user_id, movie_id, watched_on, rating, comment)
        )
        db.commit()

    @staticmethod
    def get_entries_for_user(user_id):
        db = get_db()
        return db.execute(
            'SELECT de.*, m.title FROM diary_entries de JOIN movies m ON de.movie_id = m.id WHERE de.user_id = ? ORDER BY watched_on DESC',
            (user_id,)
        ).fetchall()

    @staticmethod
    def get_entry(entry_id):
        db = get_db()
        return db.execute('SELECT * FROM diary_entries WHERE id = ?', (entry_id,)).fetchone()


diary_repository = DiaryRepository()