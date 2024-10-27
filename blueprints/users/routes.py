from flask import g, redirect, url_for, flash, render_template, abort, request, session
from security.decorators import is_admin, is_fully_authenticated
from blueprints.users import bp
from blueprints.pages import bp as base_bp
from blueprints.users.forms import RegisterUserForm, EditUserRoleForm, UserSettingsForm, UserPasswordResetForm
from persistence.repository.user import UserRepository
from persistence.model.user import User


@bp.route('/', methods=['GET', 'POST'])
@is_fully_authenticated
@is_admin
def list_all():
    users = UserRepository.find_all()
    role_form = EditUserRoleForm()

    if role_form.validate_on_submit():
        user = UserRepository.find_by_id(role_form.user_id.data) or abort(404)
        if user.is_super_admin or g.user.id == user.id:
            abort(403)

        user.role = role_form.role.data
        user.save()
        return redirect(url_for('users.list_all'))

    return render_template("users/list.html", users=users, role_form=role_form)


@bp.route('/delete/<int:user_id>', methods=['POST'])
@is_fully_authenticated
@is_admin
def delete(user_id):
    user = UserRepository.find_by_id(user_id) or abort(404)
    if user.is_super_admin or g.user.id == user.id:
        abort(403)

    username = user.name
    user.delete()
    flash(f"{username} fiókja sikeresen törölve.", 'success')
    return redirect(url_for('users.list_all'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterUserForm()
    user = User()
    if form.validate_on_submit():
        if UserRepository.find_by_name(form.name.data.strip()):
            flash('A név már foglalt!', 'error')
            return redirect(url_for('users.register'))
        user.form_update(form)
        user.save()
        flash("Sikeres regisztráció!", 'success')

        return redirect(url_for('security.login'))

    return render_template('users/register.html', form=form)


@base_bp.route('/settings')
@is_fully_authenticated
def settings():

    user_settings_form = UserSettingsForm()
    user_password_form = UserPasswordResetForm()

    user_settings_form.name.data = g.user.name

    return render_template('users/settings.html', user_settings_form=user_settings_form, user_password_form=user_password_form)


@bp.route('/user_settings', methods=['POST'])
@is_fully_authenticated
def user_settings():
    user = g.user
    user_settings_form = UserSettingsForm()

    if user_settings_form.validate_on_submit():
        if UserRepository.find_by_name(user_settings_form.name.data.strip()):
            flash('A név már foglalt!', 'error')
            return redirect(url_for('pages.settings'))

        user.name = user_settings_form.name.data
        user.save()

        flash("A felhasználónév megváltozott!.", 'success')

    return redirect(url_for('pages.settings'))


@bp.route('/password_reset', methods=['POST'])
@is_fully_authenticated
def password_reset():
    user = g.user
    user_password_form = UserPasswordResetForm()

    if user_password_form.validate_on_submit():
        if user.check_password(user_password_form.old_password.data):
            user.password = user_password_form.new_password.data
            user.save()
        else:
            flash("A régi jelszó hibás!", 'error')

    return redirect(url_for('pages.settings'))