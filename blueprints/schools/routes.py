from flask import render_template, redirect, flash, url_for, request
from .forms import CreateSchoolForm, EditSchoolForm
from persistence.model.school import School
from persistence.repository.school import SchoolRepository
from . import bp
from security.decorators import is_admin, is_fully_authenticated
from persistence.model.user import User


@bp.route('/create', methods=['GET', 'POST'])
@is_fully_authenticated
@is_admin
def create():
    form = CreateSchoolForm()

    if form.validate_on_submit():
        user = User()
        user.form_update(form)

        school = School()
        school.form_update(form)
        school.save()

        user.school_id = school.id
        user.save()

        flash("Sikeresen regisztrálta az iskolát!", 'success')
        return redirect(url_for("pages.home"))

    return render_template('schools/form.html', form=form)


@bp.route('/edit/<int:school_id>', methods=['GET', 'POST'])
@is_fully_authenticated
@is_admin
def edit(school_id):
    school = SchoolRepository.find_by_id(school_id)
    form = EditSchoolForm(obj=school)

    if form.validate_on_submit():
        school.form_update(form)
        school.save()
        flash("Sikeresen mentette az iskolát!", 'success')
        return redirect(url_for("pages.home"))

    return render_template('schools/form.html', form=form)


@bp.route('/validate-name', methods=['POST'])
@is_fully_authenticated
@is_admin
def validate_name():
    school_name = request.form.get('school_name')
    if not school_name:
        return ''

    school = SchoolRepository.find_by_name(school_name)
    if school:
        return '<div class="text-danger">A megadott név már foglalt"></div>'
    else:
        return '<div class="text-success">A megadott név nem foglalt"></div>'
