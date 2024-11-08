from flask_wtf.file import FileAllowed, FileField, FileSize
from blueprints.users.forms import RegisterUserForm
from wtforms.fields.simple import StringField, EmailField
from wtforms.validators import Length, DataRequired


class SchoolForm(RegisterUserForm):
    school_name = StringField("Iskola neve", validators=[DataRequired(), Length(min=4, max=255)])
    contact_name = StringField("Kapcsolattartó neve", validators=[DataRequired(), Length(min=3, max=128)])
    address = StringField("Iskola címe", validators=[DataRequired(), Length(min=3, max=255)])
    contact_email = EmailField("Kapcsolattartó email", validators=[DataRequired(), Length(max=128)])
    application_form = FileField('Jelentkezési lap (max. 8 MB, megengedett fájltípusok: pdf, docx, doc, rtf, odt)',
                                 validators=[FileAllowed(['pdf', 'docx', 'doc', 'rtf', 'odt'], message="Rossz fájltípus!"),
                                             FileSize(max_size=8 * 1024 * 1024, message="A fájl maximum 8 MB lehet!")])

