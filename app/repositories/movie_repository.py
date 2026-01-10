from app.db import get_db

class MovieRepository:
    @staticmethod
    def get_by_id(movie_id):
        db = get_db()
        return db.execute('SELECT * FROM movies WHERE id = ?', (movie_id,)).fetchone()

    @staticmethod
    def get_by_title(title):
        db = get_db()
        return db.execute('SELECT * FROM movies WHERE title = ?', (title,)).fetchone()

    @staticmethod
    def create(title, year=None, genre=None, description=None):
        db = get_db()
        try:
            db.execute(
                'INSERT INTO movies (title, year, genre, description) VALUES (?, ?, ?, ?)',
                (title, year, genre, description)
            )
            db.commit()
        except Exception:
            pass
        return MovieRepository.get_by_title(title)

    @staticmethod
    def get_all():
        db = get_db()
        return db.execute('SELECT * FROM movies ORDER BY title').fetchall()

movie_repository = MovieRepository()