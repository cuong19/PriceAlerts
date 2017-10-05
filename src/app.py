from flask import Flask, render_template, session, url_for
from werkzeug.utils import redirect

from src.common.database import Database

from src.models.alerts.views import alert_blueprint
from src.models.stores.views import store_blueprint
from src.models.users.views import user_blueprint

app = Flask(__name__)
app.config.from_object('src.config')
app.secret_key = "123XYZ"


@app.before_first_request
def init_db():
    Database.initialize()


@app.route("/")
def home():
    try:
        session['email']
    except KeyError:
        session['email'] = None
    if session['email'] is not None:
        return redirect(url_for("alerts.index"))
    else:
        return render_template('welcome.html')


app.register_blueprint(user_blueprint, url_prefix='/users')
app.register_blueprint(store_blueprint, url_prefix='/stores')
app.register_blueprint(alert_blueprint, url_prefix='/alerts')
