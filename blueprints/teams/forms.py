from wtforms.fields.simple import StringField
from wtforms.fields.numeric import IntegerField
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired, length, NumberRange
from blueprints.users.forms import RegisterUserForm
from persistence.repository.category import CategoryRepository
from persistence.repository.language import LanguageRepository
from persistence.repository.school import SchoolRepository


class RegisterTeamForm(RegisterUserForm):
    team_name = StringField('Csapat neve', validators=[DataRequired(), length(max=64)])
    name1 = StringField('Első csapattag neve', validators=[DataRequired(), length(max=64)])
    name2 = StringField('Masodik csapattag neve', validators=[length(max=64), DataRequired()])
    name3 = StringField('Harmadik csapattag neve', validators=[length(max=64), DataRequired()])
    name_extra = StringField('Póttag neve', validators=[length(max=64)])
    year1 = IntegerField('Első csapattag évfolyama', validators=[DataRequired(), NumberRange(min=9, max=13)])
    year2 = IntegerField('Masodik csapattag évfolyama', validators=[DataRequired(), NumberRange(min=9, max=13)])
    year3 = IntegerField('Harmadik csapattag évfolyama', validators=[DataRequired(), NumberRange(min=9, max=13)])
    year_extra = IntegerField('Póttag évfolyama', validators=[NumberRange(min=9, max=13)])
    teachers = StringField('Felkészítő tanárok (több is megadható, vesszővel elválasztva, pl.: Nagy Ferenc, Kovács János)',
                           validators=[DataRequired(), length(max=255)])

    language_id = SelectField('Választott programnyelv', validators=[DataRequired()], choices=[(0, "Még nem választok")])
    school_id = SelectField('Iskola neve', validators=[DataRequired()], choices=[(0, "Még nem választok")])
    category_id = SelectField('Kategória', validators=[DataRequired()], choices=[(0, "Még nem választok")])

    def set_dropdown_choices(self):
        self.school_id.choices = [(school.id, school.name) for school in SchoolRepository.find_all()]
        self.language_id.choices = [(language.id, language.language_name) for language in LanguageRepository.find_all()]
        self.category_id.choices = [(category.id, category.category_name) for category in CategoryRepository.find_all()]
