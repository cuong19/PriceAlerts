from flask import Blueprint, request, session, url_for, render_template
from werkzeug.utils import redirect

from src.models.users.user import User
from src.models.users.errors import UserError

user_blueprint = Blueprint('users', __name__)


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            if User.is_login_valid(email, password):
                session['email'] = email
                return redirect(url_for("alerts.index"))
        except UserError as e:
            return e.message

    return render_template("users/login.html")


@user_blueprint.route('/logout')
def logout_user():
    session['email'] = None
    return redirect(url_for('home'))


@user_blueprint.route('/signup', methods=['GET', 'POST'])
def signup_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            if User.register_user(email, password):
                session['email'] = email
                return redirect(url_for("alerts.index"))
        except UserError as e:
            return e.message

    return render_template("users/signup.html")
