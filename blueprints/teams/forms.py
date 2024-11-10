from random import choices

from wtforms.fields.simple import StringField
from wtforms.fields.numeric import IntegerField
from wtforms.fields.choices import SelectField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, length, NumberRange, Length, Optional, ValidationError
from persistence.repository.category import CategoryRepository
from persistence.repository.language import LanguageRepository
from persistence.repository.school import SchoolRepository
from blueprints.users.forms import RegisterUserForm
from persistence.repository.team import TeamRepository


class OptionalIfFieldEqualTo(Optional):
    # a validator which makes a field optional if
    # another field has a desired value

    def __init__(self, other_field_name, value, *args, **kwargs):
        self.other_field_name = other_field_name
        self.value = value
        super(OptionalIfFieldEqualTo, self).__init__(*args, **kwargs)

    def __call__(self, form, field):
        other_field = form._fields.get(self.other_field_name)
        if other_field is None:
            raise Exception('no field named "%s" in form' % self.other_field_name)
        if other_field.data == self.value:
            super(OptionalIfFieldEqualTo, self).__call__(form, field)


class EditTeamForm(FlaskForm):
    name1 = StringField('Első csapattag neve', validators=[DataRequired(), length(max=64)])
    name2 = StringField('Masodik csapattag neve', validators=[length(max=64), DataRequired()])
    name3 = StringField('Harmadik csapattag neve', validators=[length(max=64), DataRequired()])
    name_extra = StringField('Póttag neve', validators=[length(max=64), OptionalIfFieldEqualTo('year_extra', '')])
    year1 = IntegerField('Első csapattag évfolyama (9-13)', validators=[DataRequired(), NumberRange(min=9, max=13, message="Az évfolyamnak9-13 között kell lennie!")])
    year2 = IntegerField('Masodik csapattag évfolyama (9-13)', validators=[DataRequired(), NumberRange(min=9, max=13, message="Az évfolyamnak9-13 között kell lennie!")])
    year3 = IntegerField('Harmadik csapattag évfolyama (9-13)', validators=[DataRequired(), NumberRange(min=9, max=13, message="Az évfolyamnak9-13 között kell lennie!")])
    year_extra = IntegerField('Póttag évfolyama (9-13)', validators=[NumberRange(min=9, max=13, message="Az évfolyamnak9-13 között kell lennie!"), OptionalIfFieldEqualTo('name_extra', '')])
    teachers = StringField('Felkészítő tanárok (több is megadható, vesszővel elválasztva, pl.: Nagy Ferenc, Kovács János)',
                           validators=[DataRequired(), length(max=255)])

    language_id = SelectField('Választott programnyelv', validators=[DataRequired()], choices=[(0, "Még nincs itt a sajátom")])
    school_id = SelectField('Iskola neve', validators=[DataRequired()], choices=[(0, "Még nincs itt a sajátom")])
    category_id = SelectField('Kategória', validators=[DataRequired()], choices=[(0, "Még nincs itt a sajátom")])

    def set_dropdown_choices(self):
        self.school_id.choices += [(school.id, school.school_name) for school in SchoolRepository.find_all()]
        self.language_id.choices += [(language.id, language.name) for language in LanguageRepository.find_all()]
        self.category_id.choices += [(category.id, category.name) for category in CategoryRepository.find_all()]


def team_name_in_use(form, field):
    if TeamRepository.find_by_name(field.data.strip()):
        raise ValidationError('A csapatnév már foglalt!')


class CreateTeamForm(EditTeamForm, RegisterUserForm):
    team_name = StringField('Csapat neve', validators=[DataRequired(), length(max=64), team_name_in_use])


class SearchTeamsForm(FlaskForm):
    query = StringField('Keresendő szöveg', validators=[Length(max=255)])
    ascending = SelectField('Sorrend?', choices=[(0, "Csökkenő"), (1, "Növekvő")], validators=[DataRequired()])
    year = IntegerField('Osztály', validators=[NumberRange(max=13, min=9)])

    language_id = SelectField('Választott programnyelv',
                              choices=[(-1, 'Nincs szűrés'), (0, "Üresen van hagyva")])
    school_id = SelectField('Iskola neve', choices=[(-1, 'Nincs szűrés'), (0, "Üresen van hagyva")])
    category_id = SelectField('Kategória', choices=[(-1, 'Nincs szűrés'), (0, "Üresen van hagyva")])

    status = SelectField('Álapot', choices=[(-1, 'Még nincs ellenőrizve'), (0, 'Hiányos'),
                                            (1, 'Iskola által elfogadott'), (2, 'Mindenki által elfogadott')]) #todo jobb szöveg

    def set_dropdown_choices(self):
        self.school_id.choices += [(school.id, school.school_name) for school in SchoolRepository.find_all()]
        self.language_id.choices += [(language.id, language.name) for language in LanguageRepository.find_all()]
        self.category_id.choices += [(category.id, category.name) for category in CategoryRepository.find_all()]