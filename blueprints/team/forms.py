from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField
from wtforms.validators import DataRequired, length


class TeamForm(FlaskForm):
    team_name = StringField('Csapat neve', validators=[DataRequired(), length(max=64)])
    name1 = StringField('Név', validators=[DataRequired(), length(max=64)])