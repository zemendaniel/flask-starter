from flask import Blueprint, render_template
from flask_wtf.csrf import CSRFError

bp = Blueprint('team', __name__)

from blueprints.team import routes
