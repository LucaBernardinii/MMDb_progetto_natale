from flask import Blueprint, render_template, request, redirect, url_for, flash, g
from app.repositories import post_repository, movie_repository
from .auth import login_required

bp = Blueprint('post', __name__, url_prefix='/post')

@bp.route('/')
def all_posts():
    search = request.args.get('search', '').strip()
    
    if search:
        posts = post_repository.get_all_posts()
        # Filtrare i post in base al titolo del film
        posts = [p for p in posts if search.lower() in p['title'].lower()]
    else:
        posts = post_repository.get_all_posts()
    
    posts_with_likes = []
    for post in posts:
        likes_count = post_repository.get_likes_count(post['id'])
        user_liked = g.user and post_repository.user_liked_post(g.user['id'], post['id'])
        comments = post_repository.get_comments_for_post(post['id'])
        posts_with_likes.append({
            'post': post,
            'likes_count': likes_count,
            'user_liked': user_liked,
            'comments_count': len(comments)
        })
    return render_template('post/index.html', posts_with_likes=posts_with_likes, search=search)

@bp.route('/movie/<int:movie_id>')
def movie_posts(movie_id):
    movie = movie_repository.get_by_id(movie_id)
    if not movie:
        flash('Film non trovato.')
        return redirect(url_for('post.all_posts'))
    
    posts = post_repository.get_posts_for_movie(movie_id)
    posts_with_likes = []
    for post in posts:
        likes_count = post_repository.get_likes_count(post['id'])
        user_liked = g.user and post_repository.user_liked_post(g.user['id'], post['id'])
        comments = post_repository.get_comments_for_post(post['id'])
        posts_with_likes.append({
            'post': post,
            'likes_count': likes_count,
            'user_liked': user_liked,
            'comments_count': len(comments)
        })
    return render_template('post/movie_posts.html', movie=movie, posts_with_likes=posts_with_likes)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        
        if not title:
            flash('Il titolo del film è obbligatorio.')
        elif not content:
            flash('Il contenuto del post è obbligatorio.')
        else:
            # Find or create movie
            movie = movie_repository.get_by_title(title)
            if movie is None:
                movie = movie_repository.create(title)
            
            post_repository.create_post(g.user['id'], movie['id'], content)
            flash('Post creato con successo!')
            return redirect(url_for('post.movie_posts', movie_id=movie['id']))
    
    return render_template('post/create.html')

@bp.route('/create/<int:movie_id>', methods=('GET', 'POST'))
@login_required
def create_for_movie(movie_id):
    movie = movie_repository.get_by_id(movie_id)
    if not movie:
        flash('Film non trovato.')
        return redirect(url_for('post.all_posts'))
    
    if request.method == 'POST':
        content = request.form.get('content')
        
        if not content:
            flash('Il contenuto del post è obbligatorio.')
        else:
            post_repository.create_post(g.user['id'], movie_id, content)
            flash('Post creato con successo!')
            return redirect(url_for('post.movie_posts', movie_id=movie_id))
    
    return render_template('post/create_for_movie.html', movie=movie)

@bp.route('/<int:post_id>')
def view(post_id):
    post = post_repository.get_post_by_id(post_id)
    if not post:
        flash('Post non trovato.')
        return redirect(url_for('post.all_posts'))
    
    likes_count = post_repository.get_likes_count(post_id)
    user_liked = g.user and post_repository.user_liked_post(g.user['id'], post_id)
    comments = post_repository.get_comments_for_post(post_id)
    
    return render_template('post/view.html', post=post, likes_count=likes_count, 
                         user_liked=user_liked, comments=comments)

@bp.route('/<int:post_id>/edit', methods=('GET', 'POST'))
@login_required
def edit(post_id):
    post = post_repository.get_post_by_id(post_id)
    
    if not post:
        flash('Post non trovato.')
        return redirect(url_for('post.all_posts'))
    
    if post['user_id'] != g.user['id']:
        flash('Non puoi modificare questo post.')
        return redirect(url_for('post.view', post_id=post_id))
    
    if request.method == 'POST':
        content = request.form.get('content')
        
        if not content:
            flash('Il contenuto del post è obbligatorio.')
        else:
            post_repository.update_post(post_id, content)
            flash('Post modificato con successo!')
            return redirect(url_for('post.view', post_id=post_id))
    
    return render_template('post/edit.html', post=post)

@bp.route('/<int:post_id>/delete', methods=('POST',))
@login_required
def delete(post_id):
    post = post_repository.get_post_by_id(post_id)
    
    if not post:
        flash('Post non trovato.')
        return redirect(url_for('post.all_posts'))
    
    if post['user_id'] != g.user['id']:
        flash('Non puoi eliminare questo post.')
        return redirect(url_for('post.view', post_id=post_id))
    
    movie_id = post['movie_id']
    post_repository.delete_post(post_id)
    flash('Post eliminato con successo!')
    return redirect(url_for('post.movie_posts', movie_id=movie_id))

@bp.route('/<int:post_id>/like', methods=('POST',))
@login_required
def like(post_id):
    post = post_repository.get_post_by_id(post_id)
    
    if not post:
        flash('Post non trovato.')
        return redirect(url_for('post.all_posts'))
    
    if post_repository.user_liked_post(g.user['id'], post_id):
        post_repository.remove_like(g.user['id'], post_id)
    else:
        post_repository.add_like(g.user['id'], post_id)
    
    return redirect(request.referrer or url_for('post.view', post_id=post_id))

@bp.route('/<int:post_id>/comment', methods=('POST',))
@login_required
def add_comment(post_id):
    post = post_repository.get_post_by_id(post_id)
    
    if not post:
        flash('Post non trovato.')
        return redirect(url_for('post.all_posts'))
    
    content = request.form.get('content')
    
    if not content:
        flash('Il commento non può essere vuoto.')
    else:
        post_repository.add_comment(g.user['id'], post_id, content)
        flash('Commento aggiunto!')
    
    return redirect(url_for('post.view', post_id=post_id))

@bp.route('/comment/<int:comment_id>/delete', methods=('POST',))
@login_required
def delete_comment(comment_id):
    comment = post_repository.get_comment_by_id(comment_id)
    
    if not comment:
        flash('Commento non trovato.')
        return redirect(url_for('post.all_posts'))
    
    if comment['user_id'] != g.user['id']:
        flash('Non puoi eliminare questo commento.')
        return redirect(url_for('post.view', post_id=comment['post_id']))
    
    post_id = comment['post_id']
    post_repository.delete_comment(comment_id)
    flash('Commento eliminato!')
    return redirect(url_for('post.view', post_id=post_id))

@bp.route('/comment/<int:comment_id>/edit', methods=('GET', 'POST'))
@login_required
def edit_comment(comment_id):
    comment = post_repository.get_comment_by_id(comment_id)
    
    if not comment:
        flash('Commento non trovato.')
        return redirect(url_for('post.all_posts'))
    
    if comment['user_id'] != g.user['id']:
        flash('Non puoi modificare questo commento.')
        return redirect(url_for('post.view', post_id=comment['post_id']))
    
    if request.method == 'POST':
        content = request.form.get('content')
        
        if not content:
            flash('Il commento non può essere vuoto.')
        else:
            post_repository.update_comment(comment_id, content)
            flash('Commento modificato!')
            return redirect(url_for('post.view', post_id=comment['post_id']))
    
    return render_template('post/edit_comment.html', comment=comment)
