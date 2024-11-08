from flask import Blueprint, render_template
from flask_wtf.csrf import CSRFError

bp = Blueprint('teams', __name__)

from blueprints.teams import routes
