from flask import render_template, redirect, url_for, request, session
from flask_login import LoginManager, login_required, login_user
from datacollection import app
from datacollection.forms import LoginForm
from datacollection.passwordhelper import PasswordHelper

login_manager = LoginManager(app)


@app.route("/")
def index():
    return render_template("home.html", loginform=LoginForm())


@app.route("/account")
@login_required
def account():
    return redirect(url_for("dashboard"))


@app.route("/login", methods=["POST"])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        stored_user = DB.get_user(form.loginemail.data)
        if stored_user and PH.validate_password(form.loginpassword.data, stored_user['salt'], stored_user['hashed']):
            user = User(form.loginemail.data)
            login_user(user, remember=True)
            session['username'] = form.loginemail.data
            DB.click_login(user_id=session['username'], date=datetime.datetime.utcnow())
            return redirect(url_for('account'))
        form.loginemail.errors.append("Email or password invalid")
    return render_template("home.html", loginform=form)