from flask_wtf import FlaskForm
from wtforms import ValidationError
from wtforms.fields.simple import StringField
from wtforms.validators import Length, DataRequired
from persistence.repository.language import LanguageRepository


class CreateLanguageForm(FlaskForm):
    name = StringField('Programnyelv neve', validators=[DataRequired(),
                                                        Length(min=1, max=64),
                                                        lambda form, field:
                                                            CreateLanguageForm.already_in_use(form, field)])

    @staticmethod
    def already_in_use(form, filed):
        if LanguageRepository.find_by_name(filed.data):
            raise ValidationError('Ilyen programnyelv már létezik!')
