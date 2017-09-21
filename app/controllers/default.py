from flask import render_template
from flask import flash
from flask import redirect
from flask import url_for
from app import app
from app import db
from app import login_manager
from flask_login import login_user
from flask_login import logout_user

from app.models.tables import User
from app.models.forms import LoginForm

@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()


@app.route("/index")
@app.route("/home")
@app.route("/")
def index():
    return render_template('index.html')


@app.route("/login", methods=['POST', 'GET'])
def login():
    form_login = LoginForm()
    if form_login.validate_on_submit():
        user = User.query.filter_by(username=form_login.username.data).first()
        if user and user.password == form_login.password.data:
            login_user(user)
            return redirect(url_for("index"))
            flash("Logged in.")
        else:
            flash("Ivalid login.")
    return render_template('login.html', form=form_login)

@app.route("/logout")
def logout():
    logout_user()
    flash("Logged out.")
    return redirect(url_for("login"))
