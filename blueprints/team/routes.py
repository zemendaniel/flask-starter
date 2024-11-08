from flask import redirect, url_for, render_template, request, g, flash, abort, send_file
from . import bp
from  blueprints.team.forms import RegisterTeamForm
from persistence.model.team import Team
from persistence.repository.team import TeamRepository


@bp.route('/register')
def register():
    team_form = RegisterTeamForm()

    if team_form.validate_on_submit():
        team = Team()
        team.form_update(team_form)
        team.team_form_update(team_form)
        team.role = "team"
        team.save()
        flash("Sikeresen regisztrálta a csapatot!", 'success')
        return redirect(url_for("pages.home"))

    return render_template('pages/home.html', form=form)
