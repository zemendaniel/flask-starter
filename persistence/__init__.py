from werkzeug.security import generate_password_hash
import click
from alchemical.flask import Alchemical
from flask import g
from dotenv import load_dotenv
load_dotenv()

db = Alchemical()


def init_app(app):
    app.cli.add_command(__install_command)
    app.cli.add_command(___command)
    app.before_request(__on_before_request)
    app.teardown_appcontext(__on_teardown_appcontext)

    db.init_app(app)


def install():
    db.drop_all()
    db.create_all()

    reset_admin()


def reset_admin():
    with db.Session() as session:
        admin = session.scalar(User.select().where(User.role == 'admin'))
        if admin:
            session.delete(admin)
            session.commit()
        admin = User()
        admin.name = input("Admin neve:\n").strip()
        admin.set_role("admin")
        admin.password = generate_password_hash(input("Admin jelszava (min. 4 karakter hosszú):\n"))

        session.add(admin)
        session.commit()


@click.command('install')
def __install_command():
    install()
    click.echo('Application installation successful.')


@click.command('reset-admin')
def ___command():
    reset_admin()
    click.echo('Admin reset successful.')


def __on_before_request():
    if 'session' not in g:
        g.session = db.Session()


def __on_teardown_appcontext(e):
    if 'session' in g:
        g.pop('session').close()


from persistence.model.user import User
