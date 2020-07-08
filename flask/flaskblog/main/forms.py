from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    """docstring for SearchForm."""

    search_term = StringField('Search', validators=[DataRequired()])

    submit = SubmitField('Search')
