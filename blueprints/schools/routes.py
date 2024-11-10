from flask import render_template, redirect, flash, url_for, request, abort, g, send_file
from .forms import CreateSchoolForm, EditSchoolForm
from persistence.model.school import School
from persistence.repository.school import SchoolRepository
from . import bp
from security.decorators import is_admin, is_fully_authenticated, has_role
from persistence.model.user import User
from io import BytesIO


@bp.route('/create', methods=['GET', 'POST'])
@is_fully_authenticated
@is_admin
def create():
    form = CreateSchoolForm()

    if form.validate_on_submit():
        user = User()
        user.form_update(form)
        user.role = 'school'
        user.save()

        school = School()
        school.create_form_update(form)
        school.user_id = user.id
        school.save()

        flash("Sikeresen regisztrálta az iskolát!", 'success')
        return redirect(url_for("pages.home"))
    elif form.errors:
        [flash(error, 'error') for field, errors in form.errors.items() for error in errors]

    return render_template('schools/create.html', form=form)


@bp.route('/edit/<int:school_id>', methods=['GET', 'POST'])
@is_fully_authenticated
@has_role("school", "admin", "super_admin")
def edit(school_id):
    if g.user.role == "school" and g.user.school.id != school_id:
        abort(401)

    school = SchoolRepository.find_by_id(school_id) or abort(404)
    form = EditSchoolForm()

    if form.validate_on_submit():
        if g.user.is_admin and form.application_form.data:
            abort(403)

        school.edit_form_update(form)
        school.save()
        flash("Sikeresen mentette az iskolát!", 'success')
        return redirect(url_for("schools.edit", school_id=school.id))

    form.address.data = school.address
    form.contact_name.data = school.contact_name
    form.contact_email.data = school.contact_email

    return render_template('schools/edit.html', form=form, school=school)


@bp.route('/')
@is_fully_authenticated
@is_admin
def list_all():
    schools = SchoolRepository.find_all()

    search = request.args.get('search')
    application_form = request.args.get('application_form')
    #teams_status = request.args.get('teams_status')
    ascending = request.args.get('ascending')

    if search or application_form or ascending:
        schools = SchoolRepository.search(search, not bool(ascending),
            SchoolRepository.application_form_criteria(application_form) )

    return render_template('schools/list.html', schools=schools)


@bp.route('/view')
@is_fully_authenticated
@has_role("school")
def view():
    return render_template('schools/view.html', school=g.user.school)


@bp.route('/application-form/<int:school_id>')
@is_fully_authenticated
@has_role("school", "admin", "super_admin")
def application_form(school_id):
    school = SchoolRepository.find_by_id(school_id) or abort(404)
    return send_file(BytesIO(school.application_form), mimetype='application/octet-stream', as_attachment=True,
                     download_name=f"{school.school_name}.{school.form_extension}")


@bp.route('/validate-name', methods=['POST'])
@is_fully_authenticated
@is_admin
def validate_name():
    school_name = request.form.get('school_name')
    if not school_name:
        return ''

    school = SchoolRepository.find_by_name(school_name.strip())
    if school:
        return '<div class="text-danger">A megadott név már foglalt</div>'
    else:
        return '<div class="text-success">A megadott név nem foglalt</div>'
