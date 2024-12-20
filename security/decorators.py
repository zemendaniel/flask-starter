import functools

from datetime import datetime
from persistence.repository.site_setting import SiteSettingRepository
from flask import redirect, url_for, request, g, abort, flash


def is_fully_authenticated(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('security.login', redirect=request.full_path))

        return view(**kwargs)

    return wrapped_view


def is_admin(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('security.login', redirect=request.path))
        elif not g.user.is_admin:
            abort(401)

        return view(**kwargs)

    return wrapped_view


def has_role(*roles):
    roles = [arg.lower() for arg in roles]

    def has_role_decorator(view):
        @functools.wraps(view)
        def wrapped_view(*args, **kwargs):
            if g.user.role not in roles:
                abort(401)

            return view(*args, **kwargs)

        return wrapped_view

    return has_role_decorator


def is_deadline_not_over(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not SiteSettingRepository.get_deadline():
            return view(**kwargs)

        if SiteSettingRepository.get_deadline() < datetime.now():
            flash("Sajnos a határidő már lejárt!", "error")
            abort(403)

        return view(**kwargs)

    return wrapped_view


