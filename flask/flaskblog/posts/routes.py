from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post, Comment
from flaskblog.posts.forms import PostForm, CommentForm
from flask import (
    render_template,
    url_for,
    flash,
    redirect,
    request,
    abort,
    Blueprint
)

posts = Blueprint('posts', __name__)


@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            author=current_user
        )

        db.session.add(post)
        db.session.commit()

        flash('Post created', 'success')
        return redirect(url_for('main.home'))

    return render_template(
        'create_post.html',
        title='New Post',
        form=form,
        legend='New post'
    )


@posts.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    page = request.args.get('page', 1, type=int)
    post = Post.query.get_or_404(post_id)
    comments = Comment.query\
        .filter_by(
            post=post
        )\
        .order_by(
            Comment.date_posted.desc()
        )\
        .paginate(
            per_page=6,
            page=page
        )
    form = CommentForm()
    if form.validate_on_submit():
        new_comment = Comment(
            content=form.content.data,
            post_id=post.id,
            user_id=current_user.id
        )
        db.session.add(new_comment)
        db.session.commit()

        flash('Comment added', 'success')
        return redirect(url_for('posts.post', post_id=post_id))

    return render_template(
        'post.html',
        title=post.title,
        post=post,
        form=form,
        comments=comments
    )


@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)

    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("The post is updated", 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content

    return render_template(
        'create_post.html',
        title='Update post',
        form=form,
        legend='Update post'
    )


@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post=post).all()
    if post.author != current_user:
        abort(403)

    db.session.delete(post)
    for comment in comments:
        db.session.delete(Comment.query.get(comment.id))

    db.session.commit()

    flash('Post deleted', 'success')
    return redirect(url_for('main.home'))
