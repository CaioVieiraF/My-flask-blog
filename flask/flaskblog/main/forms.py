from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    """docstring for SearchForm."""

<<<<<<< HEAD
    search_term = StringField('Pesquisar', validators=[DataRequired()])

    submit = SubmitField('Pesquisar')
=======
    search_term = StringField('Search', validators=[DataRequired()])

    submit = SubmitField('Search')
>>>>>>> 1ec085f761bb46924d4a9d61e95fdfb184505ff4
