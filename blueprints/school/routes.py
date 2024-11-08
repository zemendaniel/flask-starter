from flask import render_template, redirect, flash, url_for, request
from .forms import SchoolForm
from persistence.model.school import School
from persistence.repository.school import SchoolRepository
from . import bp
from security.decorators import is_admin, is_fully_authenticated


@bp.route('/register', methods=['GET', 'POST'])
@is_fully_authenticated
@is_admin
def register():
    form = SchoolForm()
    school = School()

    if form.validate_on_submit():
        school.form_update(form)
        school.school_form_update(form)
        school.save()
        flash("Sikeresen regisztrálta az iskolát!", 'success')
        return redirect(url_for("pages.home"))

    return render_template('schools/form.html', form=form, create=True)


@bp.route('/edit/<int:school_id>', methods=['GET', 'POST'])
@is_fully_authenticated
@is_admin
def edit(school_id):
    school = SchoolRepository.find_by_id(school_id)
    form = SchoolForm(obj=school)

    if form.validate_on_submit():
        school.form_update(form)
        school.school_form_update(form)
        school.save()
        flash("Sikeresen mentette az iskolát!", 'success')
        return redirect(url_for("pages.home"))

    return render_template('schools/form.html', form=form, create=False)


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
