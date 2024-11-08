from flask import Blueprint

bp = Blueprint('languages', __name__)

from blueprints.languages import routes