# post_repository is deprecated in this project.
# The application now focuses on movies/diary/watchlist as defined in schema.sql.
# If you need blog functionality, re-add a proper 'posts' table and implementation.

def _deprecated(*args, **kwargs):
    raise RuntimeError("post_repository is removed: blog functionality is deprecated in favor of MMDb features.")

get_all_posts = _deprecated
get_post_by_id = _deprecated
create_post = _deprecated
update_post = _deprecated
delete_post = _deprecated