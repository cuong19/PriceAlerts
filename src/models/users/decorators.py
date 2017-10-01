from functools import wraps

from flask import session, url_for, request

import src.config as config

from werkzeug.utils import redirect


def requires_login(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'email' not in session.keys() or session['email'] is None:
            return redirect(url_for('users.login_user', next=request.path))
        return func(*args, **kwargs)

    return decorated_function


def requires_being_admin(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'email' not in session.keys() or session['email'] is None:
            return redirect(url_for('users.login_user', next=request.path))
        if session['email'] not in config.ADMINS:
            return redirect(url_for('users.login_user', message="Not logged in as admin!"))
        return func(*args, **kwargs)

    return decorated_function
