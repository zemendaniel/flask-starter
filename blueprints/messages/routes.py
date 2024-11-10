from flask import render_template, flash, g, redirect, url_for, abort, request
from pyexpat.errors import messages

from persistence.repository.message import MessageRepository
from persistence.repository.team import TeamRepository
from .forms import MessageForm
from security.decorators import has_role, is_fully_authenticated, is_admin
from . import bp
from persistence.model.message import Message


@bp.route('/send/<int:team_id>', methods=['GET', 'POST'])
@is_fully_authenticated
@is_admin
def send(team_id):
    form = MessageForm()
    team = TeamRepository.find_by_id(team_id) or abort(404)

    if form.validate_on_submit():
        msg = Message()
        content = form.content.data.strip()
        content = content.replace('\n', '<br>')
        msg.content = content
        msg.team_id = team_id
        msg.sender_id = g.user.id
        msg.subject = form.subject.data.strip()
        msg.save()
        team.has_unred_messages = True
        team.save()

        flash("Üzenet sikeresen elküldve!", 'success')
        return redirect(url_for('messages.list_all'))

    return render_template('messages/send.html', form=form, team=team)


@bp.route('/')
@has_role('admin', 'super_admin', 'team')
def list_all():
    if request.args.get('search'):
        messages = MessageRepository.search(request.args.get('search'), )
    else:
        messages = MessageRepository.find_all()

    if g.user.role == 'team':
        g.user.team.has_unred_messages = False
        g.user.team.save()

    return render_template('messages/list.html', messages=messages)
