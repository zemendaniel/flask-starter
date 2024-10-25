from flask_wtf import FlaskForm
from wtforms.fields.simple import SubmitField, StringField
from wtforms.validators import DataRequired, length, EqualTo


class RegisterUserForm(FlaskForm):
    name = StringField('Név', validators=[DataRequired(), length(max=32)])
    password = StringField('Jelszó', validators=[DataRequired(), length(max=32, min=4)])
    password_again = StringField('Jelszó újra', validators=[DataRequired(), length(max=32, min=4), EqualTo('password')])
    submit = SubmitField('Létrehozás')
