from flask import (
    render_template,
    url_for,
    flash,
    redirect,
    request,
    Blueprint,
    abort
)
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post, Comment
from flaskblog.users.utils import (
    save_image,
    send_reset_email,
    send_delete_email
)
from flaskblog.users.forms import (
    RegistrationForm,
    LoginForm,
    UpdateAccountForm,
    RequestResetForm,
    RequestPasswordForm
)


users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RegistrationForm()
    if form.validate_on_submit():

        hashed_password = bcrypt.generate_password_hash(
            form.password.data
        ).decode('utf-8')

        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password
        )

        db.session.add(user)
        db.session.commit()

        flash(
            f"""
                Conta criada com sucesso!\n
                Bem-vindo {form.username.data} ao meu blog!
            """,
            'success'
        )
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Registrar', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(
            user.password,
            form.password.data
        ):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Login com sucesso', 'success')
            return redirect(
                next_page
            ) if next_page else redirect(url_for('main.home'))
        else:
            flash('Credenciais incorretas', 'danger')

    return render_template('login.html', title='Login', form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_image(form.picture.data)
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('As informações da conta foram atualizadas', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for(
        'static',
        filename=f'profile_pics/{current_user.image_file}'
    )
    return render_template(
        'account.html',
        title='Minha conta',
        image_file=image_file,
        form=form
    )


@users.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query\
        .filter_by(
            author=user
        )\
        .order_by(
            Post.date_posted.desc()
        )\
        .paginate(
            per_page=6,
            page=page
        )

    return render_template('user_post.html', posts=posts, user=user)


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('E-mail enviado. Confira sua caixa de entrada', 'info')
        return redirect(url_for('users.login'))

    return render_template(
        'reset_request.html',
        title='Recuperar senha',
        form=form
    )


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def request_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    user = User.verify_reset_token(token)

    if user is None:
        flash('Esse token foi expirado ou é inválido.', 'warning')
        return redirect(url_for('users.reset_request'))

    form = RequestPasswordForm()
    if form.validate_on_submit():

        hashed_password = bcrypt.generate_password_hash(
            form.password.data
        ).decode('utf-8')

        user.password = hashed_password
        db.session.commit()

        flash("Sua senha foi alterada com sucesso!", 'success')
        return redirect(url_for('users.login'))

    return render_template(
        'reset_token.html',
        title='Recuperar senha',
        form=form
    )


@users.route('/user/<int:user_id>/delete_user', methods=['GET', 'POST'])
@login_required
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user != current_user:
        abort(403)

    send_delete_email(user)
    flash('Um E-mail de confirmação foi enviado.', 'info')
    return redirect(url_for('users.logout'))


@users.route(
    '/user/<int:user_id>/delete_user/<token>',
    methods=['GET', 'POST']
)
def request_token_delete(user_id, token):
    user_token = User.verify_reset_token(token)

    if user_token is None:
        flash('Esse token foi expirado ou é inválido.', 'warning')
        return redirect(url_for('main.home'))

    user = User.query.get_or_404(user_id)

    comments = Comment.query.filter_by(user_id=user.id).all()
    for comment in comments:
        db.session.delete(comment)

    posts = Post.query.filter_by(author=user).all()
    for post in posts:
        db.session.delete(post)

    db.session.delete(user)
    db.session.commit()

    flash('Conta deletada', 'success')
    return redirect(url_for('main.home'))
