from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for,
    session,
)
from werkzeug.exceptions import abort

from src.models.models import session_db, Posts, User, user_group
from src.auth import login_required

bp = Blueprint("blog", __name__)


@bp.route("/")
def index():
    user_id = session.get("user")

    with session_db() as s:
        # groups_where_user_is
        query = s.query(user_group).all()
        user_groups = []
        for group in query:
            if user_id == group[0]:
                user_groups.append(group[1])
        # users_with_the_same_group
        users = set([user_id])
        for group in query:
            if group[1] in user_groups:
                users.add(group[0])

        query = s.query(Posts)
        query = query.join(User, User.id == Posts.user_id)
        query = query.where(Posts.user_id.in_((users)))
        posts = query.all()
        return render_template("blog/index.html", posts=posts)


@bp.route("/favorites")
def favorites():
    user_id = session.get("user")

    with session_db() as s:
        query = s.query(User).get(user_id)

        posts = query.favorites
        return render_template("blog/favorites.html", posts=posts)


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        user_id = session.get("user")

        with session_db() as s:
            new_post = Posts(title=title, body=body, user_id=user_id)
            s.add(new_post)
            s.commit()

            return redirect(url_for("blog.index"))
    return render_template("blog/create.html")


def get_post(id, check_author=True):
    with session_db() as s:
        query = s.query(Posts)
        query = query.join(User, User.id == Posts.user_id)
        post = query.filter(Posts.id == id).first()

        if post is None:
            abort(404, f"Post id {id} doesn't exist.")

        if check_author and post.user_id != g.user.id:
            abort(403)
    return post


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    post = get_post(id)

    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        user_id = session.get("user")
        error = None

        if not title:
            error = "Title is required."
        elif error is not None:
            flash(error)
        else:
            with session_db() as s:
                post = s.query(Posts).get(id)
                if post.user_id == user_id:
                    post.body = body
                    post.title = title
                    s.commit()
                    return redirect(url_for("blog.index"))
                else:
                    flash("Can't edit someone else's post")

    return render_template("blog/update.html", post=post)


@bp.route("/<int:id>/delete", methods=["GET", "POST"])
@login_required
def delete(id):
    user_id = session.get("user")
    get_post(id)
    with session_db() as s:
        post = s.query(Posts).get(id)
        if post.user_id == user_id:
            post = s.query(Posts).filter(Posts.id == id).delete()
            s.commit()
        else:
            flash("Can't delete someone else's post")
    return redirect(url_for("blog.index"))


@bp.route("/<int:id>/favorite", methods=["GET", "POST"])
@login_required
def favorite(id):
    user_id = session.get("user")
    with session_db() as s:
        post = s.query(Posts).get(id)
        user = s.query(User).get(user_id)
        user.favorites.append(post)
        s.commit()
    return redirect(url_for("blog.index"))


@bp.route("/<int:id>/unfavorite", methods=["GET", "POST"])
@login_required
def unfavorite(id):
    user_id = session.get("user")
    with session_db() as s:
        post = s.query(Posts).get(id)
        user = s.query(User).get(user_id)
        user.favorites.remove(post)
        s.commit()
    return redirect(url_for("blog.index"))
