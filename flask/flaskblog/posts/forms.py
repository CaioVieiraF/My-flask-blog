from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    """docstring for PostForm."""

    title = StringField(
        'Title',
        validators=[
            DataRequired()
        ]
    )

    content = TextAreaField(
        'Content',
        validators=[
            DataRequired()
        ]
    )

    submit = SubmitField('Post')


class CommentForm(FlaskForm):
    """docstring for CommentForm."""

    content = TextAreaField(
        'New Comment',
        validators=[
            DataRequired(),
            Length(max=200)
        ]
    )

    submit = SubmitField('Comment')
