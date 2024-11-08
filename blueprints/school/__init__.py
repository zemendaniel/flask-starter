from flask import Blueprint, render_template

bp = Blueprint('school', __name__)

from blueprints.school import routes
