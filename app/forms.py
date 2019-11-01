from flask_wtf import FlaskForm
from markupsafe import Markup
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired

class SubmitForm(FlaskForm):
    username = StringField('Search Username :', validators=[DataRequired()])
    submit = SubmitField('Submit')
