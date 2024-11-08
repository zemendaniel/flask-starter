from flask import redirect, url_for, render_template, request, g, flash, abort, send_file
from . import bp
from blueprints.teams.forms import RegisterTeamForm
from persistence.model.team import Team
from security.decorators import has_role, is_deadline_not_over, is_fully_authenticated, is_admin
from persistence.repository.team import TeamRepository


@bp.route('/register', methods=['GET', 'POST'])
@is_deadline_not_over
def register():
    if g.user:
        return redirect(url_for('pages.home'))

    form = RegisterTeamForm()
    form.set_dropdown_choices()

    if form.validate_on_submit():
        team = Team()
        team.form_update(form)
        team.team_form_update(form)
        team.role = "teams"
        team.save()
        flash("Sikeresen regisztrálta a csapatot!", 'success')
        return redirect(url_for("pages.home"))

    return render_template('pages/home.html', form=form, create=True)


@bp.route('/edit/<int:team_id>', methods=['GET', "POST"])
@has_role('team')
def edit(team_id):
    team = TeamRepository.find_by_id(team_id)
    form = RegisterTeamForm(obj=team)
    form.set_dropdown_choices()

    if form.validate_on_submit():
        team.form_update(request.form)
        team.team_form_update(request.form)
        team.save()
        return redirect(url_for("teams.view", team_id=team_id))

    return render_template('teams/form.html', team=team, create=False, form=form)


@bp.route('/', methods=['GET', 'POST'])
@has_role('school', 'super_admin', 'admin')
def list_all():
    query = request.args.get('search')
    user_role = g.user.role
    teams = TeamRepository.search(
        query if query else '', False,
        Team.school_approved is True if user_role != 'school' else None
    )

    if request.method == "POST":
        team = TeamRepository.find_by_id(request.form.get('id'))

        if team:
            if user_role == 'school':
                team.school_approved = not team.school_approved
            elif team.school_approved:
                team.admin_approved = not team.admin_approved

    return render_template('teams/list.html', teams=teams)


@bp.route('/validate-name', methods=['POST'])
@is_fully_authenticated
@is_admin
def validate_name():
    team_name = request.form.get('team_name')
    if not team_name:
        return ''
    team = TeamRepository.find_by_name(team_name)
    if team:
        return '<div class="text-danger">A megadott név már foglalt"></div>'
    else:
        return '<div class="text-success">A megadott név nem foglalt"></div>'
