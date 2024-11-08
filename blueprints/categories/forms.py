from flask_wtf import FlaskForm
from wtforms import ValidationError
from wtforms.fields.simple import StringField
from wtforms.validators import Length, DataRequired
from persistence.repository.category import CategoryRepository


class CreateCategoryForm(FlaskForm):
    name = StringField('Kategória neve', validators=[DataRequired(), Length(min=1, max=64),
                                                     lambda form, field: CreateCategoryForm.already_in_use(form,
                                                                                                           field)])

    @staticmethod
    def already_in_use(form, filed):
        if CategoryRepository.find_by_name(filed.data):
            raise ValidationError('Ilyen kategória már létezik!')
