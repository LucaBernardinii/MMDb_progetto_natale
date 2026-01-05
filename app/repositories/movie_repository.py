from app.db import get_db

class MovieRepository:
    @staticmethod
    def get_by_id(movie_id):
        db = get_db()
        return db.execute('SELECT * FROM movies WHERE id = ?', (movie_id,)).fetchone()

    @staticmethod
    def get_by_omdb_id(omdb_id):
        db = get_db()
        return db.execute('SELECT * FROM movies WHERE omdb_id = ?', (omdb_id,)).fetchone()

    @staticmethod
    def create(omdb_id, title, year=None, type_=None, additional_json=None):
        db = get_db()
        try:
            db.execute(
                'INSERT INTO movies (omdb_id, title, year, type, additional_json) VALUES (?, ?, ?, ?, ?)',
                (omdb_id, title, year, type_, additional_json)
            )
            db.commit()
        except Exception:
            # ignore duplicates/constraints
            pass
        return MovieRepository.get_by_omdb_id(omdb_id) if omdb_id else db.execute('SELECT * FROM movies WHERE title = ? ORDER BY id DESC', (title,)).fetchone()

movie_repository = MovieRepository()