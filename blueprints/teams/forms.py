from wtforms.fields.simple import StringField, BooleanField
from wtforms.fields.numeric import IntegerField
from wtforms.fields.choices import SelectField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, length, NumberRange, Length, Optional, ValidationError
from persistence.repository.category import CategoryRepository
from persistence.repository.language import LanguageRepository
from persistence.repository.school import SchoolRepository
from blueprints.users.forms import RegisterUserForm
from persistence.repository.team import TeamRepository
from persistence.repository.user import UserRepository


class EditTeamForm(RegisterUserForm):
    name1 = StringField('Első csapattag neve', validators=[DataRequired(), length(max=64)])
    name2 = StringField('Masodik csapattag neve', validators=[length(max=64), DataRequired()])
    name3 = StringField('Harmadik csapattag neve', validators=[length(max=64), DataRequired()])
    name_extra = StringField('Póttag neve', validators=[length(max=64), Optional()])
    year1 = IntegerField('Első csapattag évfolyama (9-13)', validators=[DataRequired(), NumberRange(min=9, max=13, message="Az évfolyamnak9-13 között kell lennie!")])
    year2 = IntegerField('Masodik csapattag évfolyama (9-13)', validators=[DataRequired(), NumberRange(min=9, max=13, message="Az évfolyamnak9-13 között kell lennie!")])
    year3 = IntegerField('Harmadik csapattag évfolyama (9-13)', validators=[DataRequired(), NumberRange(min=9, max=13, message="Az évfolyamnak9-13 között kell lennie!")])
    year_extra = IntegerField('Póttag évfolyama (9-13)', validators=[NumberRange(min=9, max=13, message="Az évfolyamnak9-13 között kell lennie!"), Optional()])
    teachers = StringField('Felkészítő tanárok (több is megadható, vesszővel elválasztva, pl.: Nagy Ferenc, Kovács János)',
                           validators=[DataRequired(), length(max=255)])

    language_id = SelectField('Választott programnyelv', validators=[DataRequired()], choices=[(0, "Még nincsenek elérhető nyelvek!")])
    school_id = SelectField('Iskola neve', validators=[DataRequired()], choices=[(0, "Még nincsenek elérhető iskolák!")])
    category_id = SelectField('Kategória', validators=[DataRequired()], choices=[(0, "Még nincsenek elérhető kategóriák!")])

    def set_dropdown_choices(self):
        self.school_id.choices = [(school.id, school.name) for school in SchoolRepository.find_all()] or self.school_id.choices
        self.language_id.choices = [(language.id, language.language_name) for language in LanguageRepository.find_all()] or self.language_id.choices
        self.category_id.choices = [(category.id, category.category_name) for category in CategoryRepository.find_all()] or self.category_id.choices


def team_name_in_use(form, field):
    if TeamRepository.find_by_name(field.data.strip()):
        raise ValidationError('A csapatnév már foglalt!')


class CreateTeamForm(EditTeamForm, RegisterUserForm):
    team_name = StringField('Csapat neve', validators=[DataRequired(), length(max=64), team_name_in_use])


class SearchTeamsForm(FlaskForm):
    query = StringField('Keresendő szöveg', validators=[Length(max=255)])
    ascending = BooleanField('Növekvő sorrend?')
    year = IntegerField('Osztály', validators=[NumberRange(max=13, min=9)])

    language_id = SelectField('Választott programnyelv', validators=[DataRequired()],
                              choices=[(0, "Üres")])
    school_id = SelectField('Iskola neve', validators=[DataRequired()], choices=[(0, "Üres")])
    category_id = SelectField('Kategória', validators=[DataRequired()], choices=[(0, "Üres")])

    def set_dropdown_choices(self):
        self.school_id.choices += [(school.id, school.name) for school in SchoolRepository.find_all()]
        self.language_id.choices += [(language.id, language.language_name) for language in LanguageRepository.find_all()]
        self.category_id.choices += [(category.id, category.category_name) for category in CategoryRepository.find_all()]