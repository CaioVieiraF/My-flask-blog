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
        'Password',
        validators=[
            DataRequired(),
            Length(min=8)
        ]
    )

    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(),
            Length(min=8),
            EqualTo('password')
        ]
    )

    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()

        if user:
            raise ValidationError('Username taken. Try a different one')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()

        if user:
            raise ValidationError('E-mail taken. Try a different one')


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
        'Password',
        validators=[
            DataRequired(),
            Length(min=8)
        ]
    )

    remember = BooleanField('Remenber Me')

    submit = SubmitField('Log In')


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
        'Update Picture',
        validators=[
            FileAllowed(['jpg', 'png'])
        ]
    )

    submit = SubmitField('Update')

    def validate_username(self, username):
        if current_user.username != username.data:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username taken. Try a different one')

    def validate_email(self, email):
        if current_user.email != email.data:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('E-mail taken. Try a different one')


class RequestResetForm(FlaskForm):
    """docstring for RequestResetForm."""

    email = StringField(
        'Email',
        validators=[
            Email(),
            DataRequired()
        ]
    )

    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()

        if user is None:
            raise ValidationError('No account for this E-mail')


class RequestPasswordForm(FlaskForm):
    """docstring for RequestPasswordForm."""

    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=8)
        ]
    )

    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(),
            Length(min=8),
            EqualTo('password')
        ]
    )

    submit = SubmitField('Reset password')
