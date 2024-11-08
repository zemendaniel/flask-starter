from flask import redirect, url_for, render_template, request, g, flash, abort, send_file
from . import bp
from persistence.model.team import Team
from blueprints.teams.forms import CreateTeamForm, EditTeamForm
from security.decorators import has_role, is_deadline_not_over, is_fully_authenticated, is_admin
from persistence.repository.team import TeamRepository
from persistence.model.user import User
from persistence.repository.user import UserRepository


@bp.route('/create', methods=['GET', 'POST'])
@is_deadline_not_over
def create():
    if g.user:
        return redirect(url_for('pages.home'))

    form = CreateTeamForm()
    form.set_dropdown_choices()

    if form.validate_on_submit():
        user = User()
        user.form_update(form)

        team = Team()
        team.team_form_update(form)
        team.save()

        user.team_id = team.id
        user.save()

        flash("Sikeresen regisztrálta a csapatot!", 'success')
        return redirect(url_for("pages.home"))

    return render_template('teams/create.html', form=form)


@bp.route('/edit/<int:team_id>', methods=['GET', "POST"])
@has_role('team')
def edit(team_id):
    team = TeamRepository.find_by_id(team_id)
    form = EditTeamForm(obj=team)
    form.set_dropdown_choices()

    if form.validate_on_submit():
        team.form_update(request.form)
        team.team_form_update(request.form)
        team.save()
        return redirect(url_for("teams.view", team_id=team_id))

    return render_template('teams/edit.html', form=form)


@bp.route('/', methods=['GET', 'POST'])
@has_role('schools', 'super_admin', 'admin')
def list_all():
    query = request.args.get('search')
    user_role = g.user.role
    teams = TeamRepository.search(
        query if query else '', False,
        Team.school == g.user.school if user_role == 'schools' else None
    )

    if request.method == "POST":
        team = TeamRepository.find_by_id(request.form.get('id'))

        if team:
            if user_role == 'schools':
                team.school_approved = not team.school_approved
            elif team.school_approved:
                team.admin_approved = not team.admin_approved

    return render_template('teams/list.html', teams=teams)


@bp.route('/validate-name', methods=['POST'])
def validate_name():
    team_name = request.form.get('team_name')
    if not team_name:
        return ''
    team = TeamRepository.find_by_name(team_name)
    if team:
        return '<div class="text-danger">A megadott név már foglalt"></div>'
    else:
        return '<div class="text-success">A megadott név nem foglalt"></div>'
