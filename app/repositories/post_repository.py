from app.db import get_db
from datetime import datetime

class PostRepository:
    @staticmethod
    def create_post(user_id, movie_id, content):
        db = get_db()
        cursor = db.execute(
            'INSERT INTO posts (user_id, movie_id, content) VALUES (?, ?, ?)',
            (user_id, movie_id, content)
        )
        db.commit()
        return cursor.lastrowid

    @staticmethod
    def get_post_by_id(post_id):
        db = get_db()
        return db.execute(
            'SELECT p.*, u.username, m.title FROM posts p '
            'JOIN users u ON p.user_id = u.id '
            'JOIN movies m ON p.movie_id = m.id '
            'WHERE p.id = ?',
            (post_id,)
        ).fetchone()

    @staticmethod
    def get_posts_for_movie(movie_id):
        db = get_db()
        return db.execute(
            'SELECT p.*, u.username, m.title FROM posts p '
            'JOIN users u ON p.user_id = u.id '
            'JOIN movies m ON p.movie_id = m.id '
            'WHERE p.movie_id = ? ORDER BY p.created_at DESC',
            (movie_id,)
        ).fetchall()

    @staticmethod
    def get_all_posts():
        db = get_db()
        return db.execute(
            'SELECT p.*, u.username, m.title FROM posts p '
            'JOIN users u ON p.user_id = u.id '
            'JOIN movies m ON p.movie_id = m.id '
            'ORDER BY p.created_at DESC'
        ).fetchall()

    @staticmethod
    def update_post(post_id, content):
        db = get_db()
        db.execute(
            'UPDATE posts SET content = ?, updated_at = ? WHERE id = ?',
            (content, datetime.now(), post_id)
        )
        db.commit()

    @staticmethod
    def delete_post(post_id):
        db = get_db()
        db.execute('DELETE FROM post_comments WHERE post_id = ?', (post_id,))
        db.execute('DELETE FROM post_likes WHERE post_id = ?', (post_id,))
        db.execute('DELETE FROM posts WHERE id = ?', (post_id,))
        db.commit()

    @staticmethod
    def add_like(user_id, post_id):
        db = get_db()
        try:
            db.execute(
                'INSERT INTO post_likes (user_id, post_id) VALUES (?, ?)',
                (user_id, post_id)
            )
            db.commit()
            return True
        except Exception:
            return False

    @staticmethod
    def remove_like(user_id, post_id):
        db = get_db()
        db.execute('DELETE FROM post_likes WHERE user_id = ? AND post_id = ?', (user_id, post_id))
        db.commit()

    @staticmethod
    def get_likes_count(post_id):
        db = get_db()
        result = db.execute('SELECT COUNT(*) as count FROM post_likes WHERE post_id = ?', (post_id,)).fetchone()
        return result['count'] if result else 0

    @staticmethod
    def user_liked_post(user_id, post_id):
        db = get_db()
        result = db.execute('SELECT 1 FROM post_likes WHERE user_id = ? AND post_id = ?', (user_id, post_id)).fetchone()
        return result is not None

    @staticmethod
    def add_comment(user_id, post_id, content):
        db = get_db()
        cursor = db.execute(
            'INSERT INTO post_comments (user_id, post_id, content) VALUES (?, ?, ?)',
            (user_id, post_id, content)
        )
        db.commit()
        return cursor.lastrowid

    @staticmethod
    def get_comments_for_post(post_id):
        db = get_db()
        return db.execute(
            'SELECT pc.*, u.username FROM post_comments pc '
            'JOIN users u ON pc.user_id = u.id '
            'WHERE pc.post_id = ? ORDER BY pc.created_at ASC',
            (post_id,)
        ).fetchall()

    @staticmethod
    def get_comment_by_id(comment_id):
        db = get_db()
        return db.execute('SELECT * FROM post_comments WHERE id = ?', (comment_id,)).fetchone()

    @staticmethod
    def update_comment(comment_id, content):
        db = get_db()
        db.execute(
            'UPDATE post_comments SET content = ?, updated_at = ? WHERE id = ?',
            (content, datetime.now(), comment_id)
        )
        db.commit()

    @staticmethod
    def delete_comment(comment_id):
        db = get_db()
        db.execute('DELETE FROM post_comments WHERE id = ?', (comment_id,))
        db.commit()


post_repository = PostRepository()