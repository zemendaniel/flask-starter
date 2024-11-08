from flask import render_template, redirect, flash, url_for
from .forms import SchoolForm
from persistence.model.school import School
from . import bp


@bp.route('/register')
def register():
    form = SchoolForm()
    school = School
    
    if form.validate_on_submit():
        school.form_update(form)
        school.school_form_update(form)
        school.save()
        flash("Sikeresen regisztrálta az iskolát!", 'success')
        return redirect(url_for("pages.home"))

    return render_template('schools/register.html', form=form)
