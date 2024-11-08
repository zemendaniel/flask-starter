from flask import render_template, redirect, flash, url_for, request, abort
from .forms import CreateSchoolForm, EditSchoolForm
from persistence.model.school import School
from persistence.repository.school import SchoolRepository
from . import bp
from security.decorators import is_admin, is_fully_authenticated, has_role
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
        school.create_form_update(form)
        school.save()

        user.school_id = school.id
        user.save()

        flash("Sikeresen regisztrálta az iskolát!", 'success')
        return redirect(url_for("pages.home"))

    return render_template('schools/create.html', form=form)


@bp.route('/edit/<int:school_id>', methods=['GET', 'POST'])
@is_fully_authenticated
@is_admin
def edit(school_id):
    school = SchoolRepository.find_by_id(school_id)
    form = EditSchoolForm(obj=school)

    if form.validate_on_submit():
        school.edit_form_update(form)
        school.save()
        flash("Sikeresen mentette az iskolát!", 'success')
        return redirect(url_for("pages.home"))

    return render_template('schools/edit.html', form=form)


@bp.route('/delete/<int:school_id>')
@is_fully_authenticated
@is_admin
def delete(school_id):
    school = SchoolRepository.find_by_id(school_id) or abort(404)
    school.delete()
    flash("Sikeresen törlte az iskolát!", 'success')
    return redirect(url_for("schools.list_all"))


@bp.route('/list')
@is_fully_authenticated
@is_admin
def list_all():
    schools = SchoolRepository.find_all()
    # todo keresés

    return render_template('schools/list.html', schools=schools)


@bp.route('/application-form/<int:school_id>')
@is_fully_authenticated
@has_role("school", "admin", "super_admin")
def application_form(school_id):
    school = SchoolRepository.find_by_id(school_id) or abort(404)
    return send_file(BytesIO(school.application_form), mimetype='application/octet-stream', as_attachment=True,
                     download_name=f"{school.name}.{school.form_extension}")


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
