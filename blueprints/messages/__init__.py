from flask import Blueprint

bp = Blueprint('messages', __name__)

from blueprints.messages import routes