from flask import redirect, url_for, render_template, request, g
from blueprints.pages import bp
from security.decorators import is_fully_authenticated, is_admin


@bp.route('/')
def home():
    return render_template('pages/home.html')


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
