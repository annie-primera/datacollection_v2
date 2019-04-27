from flask import render_template, redirect, url_for, request, session, flash
from flask_login import LoginManager, login_required, login_user
from datacollection import app, db, bcrypt
from datacollection.forms import LoginForm, RegistrationForm
from datacollection.models import User

login_manager = LoginManager(app)


@app.route("/")
def index():
    return render_template("home.html", loginform=LoginForm())


@app.route("/account")
@login_required
def account():
    return redirect(url_for("dashboard"))


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
        stored_user = DB.get_user(form.loginemail.data)
        if stored_user and PH.validate_password(form.loginpassword.data, stored_user['salt'], stored_user['hashed']):
            user = User(form.loginemail.data)
            login_user(user, remember=True)
            session['username'] = form.loginemail.data
            DB.click_login(user_id=session['username'], date=datetime.datetime.utcnow())
            return redirect(url_for('account'))
        form.loginemail.errors.append("Email or password invalid")
    return render_template("home.html", loginform=form)