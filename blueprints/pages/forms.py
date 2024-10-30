from flask_wtf import FlaskForm
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, Length


class SetOrgNameForm(FlaskForm):
    name = TextAreaField("Név", validators=[DataRequired(), Length(max=255)])
