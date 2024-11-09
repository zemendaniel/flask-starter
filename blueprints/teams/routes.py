from flask import redirect, url_for, render_template, request, g, flash, abort, session
from . import bp
from persistence.model.team import Team
from blueprints.teams.forms import CreateTeamForm, EditTeamForm, SearchTeamsForm
from security.decorators import has_role, is_deadline_not_over, is_fully_authenticated
from persistence.repository.team import TeamRepository
from persistence.model.user import User


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
        user.role = 'team'
        user.save()

        team = Team()
        team.team_form_update(form)
        team.user_id = user.id
        team.save()

        session['user_id'] = user.id

        flash("Sikeresen regisztrálta a csapatot!", 'success')
        return redirect(url_for("pages.home"))
    elif form.errors:
        [flash(error, 'error') for field, errors in form.errors.items() for error in errors]

    return render_template('teams/create.html', form=form)


@bp.route('/edit/<int:team_id>', methods=['GET', "POST"])
@is_fully_authenticated
@has_role('team', 'admin', 'super_admin')
@is_deadline_not_over
def edit(team_id):
    team = TeamRepository.find_by_id(team_id) or abort(404)
    form = EditTeamForm(obj=team)
    form.set_dropdown_choices()

    if form.validate_on_submit():
        team.team_form_update(form)
        team.save()
        flash("Sikeresen szerkesztette a csapatot!", 'success')
        return redirect(url_for("teams.edit", team_id=team_id))

    return render_template('teams/edit.html', form=form)


@bp.route('/', methods=['GET', 'POST'])
@is_fully_authenticated
@has_role('school', 'super_admin', 'admin')
def list_all():
    form = SearchTeamsForm(request.args)
    form.set_dropdown_choices()

    if form.validate():
        teams = TeamRepository.search(
            form.query,
            bool(form.ascending),
            TeamRepository.year_criteria(form.year),
            Team.language_id == form.language_id,
            Team.school_id == form.school_id,
            Team.category_id == form.category_id
        )
    else:
        teams = TeamRepository.find_all()

    if request.method == "POST":
        team = TeamRepository.find_by_id(request.form.get('team_id')) or abort(404)

        if g.user.role == 'school' and not g.user.school.application_form:
            flash("Először fel kell tölteni a jelentkezési lapot!", 'error')
            abort(403)

        if g.user.role == 'school' and team.school_id == g.user.school.id and not team.admin_approved:
            team.school_approved = not team.school_approved

        elif team.school_approved and g.user.is_admin:
            team.admin_approved = not team.admin_approved

        team.save()
        flash("A csapat sikeresen frissítve!", 'success')
        return redirect(url_for("teams.list_all"))

    return render_template('teams/list.html', teams=teams, form=form)


@bp.route('/view')
@is_fully_authenticated
@has_role("team")
def view():
    return render_template('teams/view.html', team=g.user.team)


@bp.route('/validate-name', methods=['POST'])
def validate_name():
    team_name = request.form.get('team_name')
    if not team_name:
        return ''
    team = TeamRepository.find_by_name(team_name.strip())
    if team:
        return '<div class="text-danger">A megadott név már foglalt</div>'
    else:
        return '<div class="text-success">A megadott név nem foglalt</div>'


@bp.route('/incomplete/<int:team_id>', methods=['POST'])
@is_fully_authenticated
def incomplete(team_id):
    team = TeamRepository.find_by_id(team_id) or abort(404)
    team.declared_incomplete = not team.declared_incomplete
    team.save()
    flash("Hiánypótlás állapota sikeresen frissítve!", 'success')
    return redirect(url_for('teams.list_all'))
