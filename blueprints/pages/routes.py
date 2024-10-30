from flask import redirect, url_for, render_template, request, g, flash, abort, send_file
from blueprints.pages import bp
from security.decorators import is_fully_authenticated, is_admin
from blueprints.pages.forms import SetOrgNameForm, SetFaviconForm
from persistence.repository.site_setting import SiteSettingRepository
from io import BytesIO


@bp.route('/')
def home():
    return render_template('pages/home.html')


@bp.route('/site-settings', methods=['GET', 'POST'])
@is_fully_authenticated
@is_admin
def site_settings():
    org_form = SetOrgNameForm()
    icon_form = SetFaviconForm()

    if org_form.validate_on_submit():
        SiteSettingRepository.set_org_name(org_form.name.data.strip())
        flash("A szervezet neve sikeresen beállítva!", 'success')
    else:
        org_form.name.data = SiteSettingRepository.get_org_name()

    if icon_form.validate_on_submit():
        SiteSettingRepository.set_favicon(icon_form.icon.data)
        flash("A favicon sikeresen beállítva!"
              "|Lehetséges, hogy üríteni kell a gyorsítótárat, hogy az új ikon jelenjen meg.", 'success')
        return redirect(url_for('pages.site_settings'))

    return render_template('pages/site-settings.html', org_form=org_form, icon_form=icon_form,
                           favicon_exits=bool(SiteSettingRepository.find_by_key('favicon')))


@bp.route('/delete-favicon', methods=['POST'])
@is_fully_authenticated
@is_admin
def delete_favicon():
    icon = SiteSettingRepository.find_by_key('favicon') or abort(404)
    SiteSettingRepository.delete(icon)
    flash("A favicon sikeresen törölve!|Lehetséges, hogy üríteni kell a gyorsítótárat,"
          " hogy a változtatások látszódjanak.", 'success')
    return redirect(url_for('pages.site_settings'))


@bp.route('/favicon.ico')
def favicon():
    icon = SiteSettingRepository.get_favicon() or abort(404)

    return send_file(BytesIO(icon), mimetype='application/octet-stream', as_attachment=False, download_name='favicon.ico')


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


@bp.route("/about")
def about():
    return render_template("pages/about.html")
