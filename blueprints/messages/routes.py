from flask import render_template

from . import bp


@bp.route('/')
def send():

    return render_template('messages/send.html')

