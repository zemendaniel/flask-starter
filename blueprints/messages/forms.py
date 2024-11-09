from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length
from wtforms.fields.simple import TextAreaField, StringField


class MessageForm(FlaskForm):
    content = TextAreaField("Üzenet", validators=[DataRequired(), Length(max=4096)])
    subject = StringField("Tárgy", validators=[DataRequired(), Length(max=255)])
