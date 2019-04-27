from flask import render_template, redirect, url_for, request, session, flash
from flask_login import login_required, login_user, logout_user, current_user
from datacollection import app, db, bcrypt
from datacollection.forms import LoginForm, RegistrationForm
from datacollection.models import User, UserActions, Texts


@app.route("/")
def index():
    return render_template("home.html", loginform=LoginForm())


@app.route("/account")
@login_required
def account():
    return redirect(url_for('dashboard'))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        form = RegistrationForm(request.form)
        if form.validate_on_submit():
            if User.query.filter_by(email=form.email.data).first():
                form.email.errors.append("Email address already registered")
                return render_template("registration.html", registrationform=form)
            hashedpassword = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
            user = User(email=form.email.data, password=hashedpassword)
            db.session.add(user)
            db.session.commit()
            return render_template("home.html", onloadmessage="Registration successful. Please log in.", loginform=LoginForm())
        return render_template("registration.html", registrationform=form)
    registrationform = RegistrationForm()
    return render_template("registration.html", registrationform=registrationform)


@app.route("/login", methods=["POST"])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.loginemail.data).first()
        if user and bcrypt.check_password_hash(user.password, form.loginpassword.data):
            login_user(user, remember=True)
            login_click = UserActions(action=1, user_id=user.id)
            db.session.add(login_click)
            db.session.commit()
            return redirect(url_for('account'))
        else:
            form.loginemail.errors.append("Email or password invalid")
    return render_template("home.html", loginform=form)


@app.route("/logout", methods=["POST"])
def logout():
    logout_user()
    return render_template("home.html", loginform=LoginForm())


@app.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    texts = Texts.query.filter_by(user_id=current_user.id).first()
    return render_template("dashboard.html", texts=texts)
