from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from flask_login import current_user
from flaskblog.models import User
from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    EqualTo,
    ValidationError
)


class RegistrationForm(FlaskForm):
    """docstring for RegistrationForm."""

    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Length(min=5, max=25)
        ]
    )

    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField(
        'Senha',
        validators=[
            DataRequired(),
            Length(min=8)
        ]
    )

    confirm_password = PasswordField(
        'Confirmar senha',
        validators=[
            DataRequired(),
            Length(min=8),
            EqualTo('password')
        ]
    )

    submit = SubmitField('Registrar')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()

        if user:
            raise ValidationError('Esse username já tem dono! Tente um diferente')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()

        if user:
            raise ValidationError('Esse E-mail já tem dono! Tente um diferente')


class LoginForm(FlaskForm):
    """docstring for LoginForm."""

    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField(
        'Senha',
        validators=[
            DataRequired(),
            Length(min=8)
        ]
    )

    remember = BooleanField('Lembrar de mim')

    submit = SubmitField('LogIn')


class UpdateAccountForm(FlaskForm):
    """docstring for RegistrationForm."""

    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Length(min=5, max=25)
        ]
    )

    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email()
        ]
    )

    picture = FileField(
        'Mudar foto',
        validators=[
            FileAllowed(['jpg', 'png'])
        ]
    )

    submit = SubmitField('Atualizar')

    def validate_username(self, username):
        if current_user.username != username.data:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Esse username já tem dono! Tente um diferente')

    def validate_email(self, email):
        if current_user.email != email.data:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Esse username já tem dono! Tente um diferente')


class RequestResetForm(FlaskForm):
    """docstring for RequestResetForm."""

    email = StringField(
        'Email',
        validators=[
            Email(),
            DataRequired()
        ]
    )

    submit = SubmitField('Solicitar nova senha')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()

        if user is None:
            raise ValidationError('Não existe nenhuma conta com esse E-mail')


class RequestPasswordForm(FlaskForm):
    """docstring for RequestPasswordForm."""

    password = PasswordField(
        'Nova senha',
        validators=[
            DataRequired(),
            Length(min=8)
        ]
    )

    confirm_password = PasswordField(
        'Confirmar senha',
        validators=[
            DataRequired(),
            Length(min=8),
            EqualTo('password')
        ]
    )

    submit = SubmitField('Mudar senha')
