# todo private post shows up in amount bug fix
# todo fix activity css

import os
import threading
import logging
import persistence
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template
from mail_backup import send_mail
import blueprints.posts
import blueprints.security
import blueprints.pages
import blueprints.users
import blueprints.activites
import security
from flask_wtf.csrf import CSRFProtect, CSRFError
from config import Config
import garmin_api
from flask_minify import Minify

csrf = CSRFProtect()
minify = Minify(html=True, js=True, cssless=True)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_size': 10,  # The number of connections to keep in the pool
        'max_overflow': 20,  # The number of connections to allow beyond the pool size
        'pool_timeout': 30,  # Timeout in seconds before giving up on getting a connection from the pool
        'pool_recycle': 1800,  # Recycle connections after this number of seconds
    }
    persistence.init_app(app)
    security.init_app(app)
    csrf.init_app(app)
    garmin_api.init_app(app)
    minify.init_app(app)

    app.register_blueprint(blueprints.posts.bp, url_prefix='/posts')
    app.register_blueprint(blueprints.pages.bp, url_prefix='/')
    app.register_blueprint(blueprints.security.bp, url_prefix='/')
    app.register_blueprint(blueprints.users.bp, url_prefix='/users')
    app.register_blueprint(blueprints.activites.bp, url_prefix='/activities')

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

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template('errors/400.html'), 400

    if os.environ['PROD'] == 'true':
        threading.Thread(target=send_mail, daemon=True).start()

    return app


if __name__ == '__main__':
    create_app().run(host="0.0.0.0", debug=False)

