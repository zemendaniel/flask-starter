# todo Adam css dolgok
# todo Adam valahol jelenlen meg magyarul a jogosultság (g.user.role_hun)
# todo Adam dark mode legyen vagy ne legyen
# todo settings page

import os
import logging
import persistence
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template
import blueprints.posts
import blueprints.security
import blueprints.pages
import blueprints.users
import security
from flask_wtf.csrf import CSRFProtect, CSRFError
from config import Config
from flask_minify import Minify
from jinja2 import Environment, PackageLoader, select_autoescape

csrf = CSRFProtect()
minify = Minify(html=True, js=True, cssless=True)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.jinja_env.add_extension('jinja2.ext.do')
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_size': 10,
        'max_overflow': 20,
        'pool_timeout': 30,
        'pool_recycle': 1800,
    }
    persistence.init_app(app)
    security.init_app(app)
    csrf.init_app(app)
    minify.init_app(app)

    app.register_blueprint(blueprints.posts.bp, url_prefix='/posts')
    app.register_blueprint(blueprints.pages.bp, url_prefix='/')
    app.register_blueprint(blueprints.security.bp, url_prefix='/')
    app.register_blueprint(blueprints.users.bp, url_prefix='/users')

    handler = RotatingFileHandler('errors.log')
    handler.setLevel(logging.ERROR)
    app.logger.addHandler(handler)

    @app.errorhandler(500)
    def internal_server_error(error):
        app.logger.error('Server Error: %s', error)
        return render_template('errors/500.html'), 500

    @app.errorhandler(404)
    def not_found(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(401)
    def unauthorized(error):
        return render_template('errors/401.html'), 401

    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html'), 403

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template('errors/403.html'), 400

    return app


if __name__ == '__main__':
    create_app().run(host="0.0.0.0", debug=True)

