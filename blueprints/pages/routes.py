from flask import redirect, url_for, render_template, request, g, flash
from blueprints.pages import bp
from security.decorators import is_fully_authenticated, is_admin
from blueprints.pages.forms import SetOrgNameForm
from persistence.repository.site_setting import SiteSettingRepository


@bp.route('/')
def home():
    return render_template('pages/home.html')


@bp.route('/site-settings', methods=['GET', 'POST'])
@is_fully_authenticated
@is_admin
def site_settings():
    org_form = SetOrgNameForm()

    if org_form.validate_on_submit():
        SiteSettingRepository.set_org_name(org_form.name.data.strip())
        flash("A szervezet neve sikeresen beállítva!", 'success')
    else:
        org_form.name.data = SiteSettingRepository.get_org_name()

    return render_template('pages/site-settings.html', org_form=org_form)


@bp.route('/errors')
@is_fully_authenticated
@is_admin
def errors():
    if request.args.get('delete'):
        with open('errors.log', 'w') as f:
            f.write('')
        return redirect(url_for('pages.errors'))

    try:
        with open('errors.log', 'r') as f:
            errors_text = f.read().replace('\n', '<br>')
    except FileNotFoundError:
        errors_text = ""

    return render_template("errors/errors.html", errors=errors_text)
