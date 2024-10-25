from flask import g, redirect, url_for, flash, render_template, abort, session
from security.decorators import is_admin, is_fully_authenticated
from blueprints.users import bp
from blueprints.users.forms import RegisterUserForm
from persistence.repository.user import UserRepository
from persistence.model.user import User


@bp.route('/')
@is_fully_authenticated
@is_admin
def list_all():
    users = UserRepository.find_all()

    return render_template("users/list.html", users=users)


@bp.route('/delete/<int:user_id>', methods=['POST'])
@is_fully_authenticated
@is_admin
def delete(user_id):
    user = UserRepository.find_by_id(user_id) or abort(404)
    if user.role == 'admin':
        abort(401)

    username = user.name
    user.delete()
    flash(f"{username} fiókja sikeresen törölve.", 'success')
    return redirect(url_for('users.list_all'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterUserForm()
    if form.validate_on_submit():
        if UserRepository.find_by_name(form.name.data.strip()):
            flash('A név már foglalt!', 'error')
            return redirect(url_for('users.create'))
        user = User()
        user.name = form.name.data.strip()
        user.role = "user"
        user.save()
        flash("Sikeres regisztráció!", 'success')
        return redirect(url_for('security.login'))

    return render_template('users/register.html', form=form)
