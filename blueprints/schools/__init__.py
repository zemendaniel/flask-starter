from flask import Blueprint, render_template

bp = Blueprint('schools', __name__)

from blueprints.schools import routes
