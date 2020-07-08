from flaskblog.models import Post
from flask import (
    render_template,
    request,
    Blueprint,
    redirect,
    url_for
)

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(
        Post.date_posted.desc()
    ).paginate(
        per_page=6,
        page=page
    )

    return render_template('home.html', posts=posts)


@main.route('/about')
def about():
    return render_template('about.html', title='Sobre')


@main.route('/search/<string:tags>', methods=['GET', 'POST'])
def search(tags=None):
    if not tags:
        return redirect(url_for('main.home'))
    page = request.args.get('page', 1, type=int)
    post_list = [
        post.id for post in Post.query.all()
        if tags in post.tags
    ]

    posts = Post.query\
        .filter(
            Post.id.in_(post_list)
        )\
        .order_by(
            Post.date_posted.desc()
        )\
        .paginate(
            per_page=6,
            page=page
        )

    return render_template(
        'search.html',
        title='Search',
        tags=tags,
        posts=posts
    )
