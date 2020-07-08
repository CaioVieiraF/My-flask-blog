from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    """docstring for PostForm."""

    title = StringField(
        'Título',
        validators=[
            DataRequired()
        ]
    )

    description = StringField('Descrição')

    content = TextAreaField(
        'Conteudo',
        validators=[
            DataRequired()
        ]
    )

    tags = StringField('tags')

    submit = SubmitField('Post')


class CommentForm(FlaskForm):
    """docstring for CommentForm."""

    content = TextAreaField(
        'Novo comentário',
        validators=[
            DataRequired(),
            Length(max=200)
        ]
    )

    submit = SubmitField('Comentar')
