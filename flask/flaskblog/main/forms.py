from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    """docstring for SearchForm."""

    search_term = StringField('Pesquisar', validators=[DataRequired()])

    submit = SubmitField('Pesquisar')
