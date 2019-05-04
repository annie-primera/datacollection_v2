from flask import render_template, redirect, url_for, request, abort, flash
from flask_login import login_required, login_user, logout_user, current_user
from datacollection import app, db, bcrypt
from datacollection.forms import LoginForm, RegistrationForm, NewPost, EditPost
from datacollection.models import User, UserActions, Texts, TextVersions
from datacollection.grammar import Grammar
from bs4 import BeautifulSoup


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
    texts = Texts.query.filter_by(user_id=current_user.id).all()
    return render_template("dashboard.html", texts=texts)


@app.route("/newtext", methods=["GET", "POST"])
@login_required
def newtext():
    form = EditPost()
    if request.method == "POST":
        title = request.form['title']
        text = request.form['text']
        new_text = Texts(user_id=current_user.id, title=title, content=text)
        db.session.add(new_text)
        db.session.commit()
        last_text = db.session.query(Texts).order_by(Texts.id.desc()).first()
        text_version = TextVersions(content=last_text.content, user_id=current_user.id, text_id=last_text.id)
        db.session.add(text_version)
        db.session.commit()
        new_click = UserActions(user_id=current_user.id, action=4)
        db.session.add(new_click)
        db.session.commit()
        plaintext = BeautifulSoup(last_text.content)
        text_summary = Grammar.summary(plaintext.get_text())
        return render_template("summary.html", text_id=last_text.id, text_summary=text_summary)
    elif request.method == "GET":
        return render_template("basiceditor.html", form=form)


@app.route("/editor/<text_id>", methods=["GET", "POST"])
@login_required
def editor(text_id):
    text = Texts.query.get_or_404(text_id)
    if text.user_id != current_user.id:
        abort(403)
    form = EditPost()
    if request.method == "POST" and form.validate():
        text.title = form.title.data
        text.content = form.content.data
        db.session.commit()
        new_click = UserActions(user_id=current_user.id, action=3)
        db.session.add(new_click)
        db.session.commit()
        text_version = TextVersions(content=form.content.data, user_id=current_user.id, text_id=text_id)
        db.session.add(text_version)
        db.session.commit()
        return redirect(url_for('dashboard'))
    elif request.method == "GET":
        form.content.data = text.content
        form.title.data = text.title
        text_id = Texts.query.get_or_404(text_id)
        return render_template("editor.html", form=form, text_id=text_id)


@app.route("/summary/<text_id>", methods=["POST"])
@login_required
def summary(text_id):
    texts = Texts.query.filter_by(id=text_id).first()
    text = texts.content
    text_version = TextVersions(content=text, user_id=current_user.id, text_id=text_id)
    db.session.add(text_version)
    db.session.commit()
    plaintext = BeautifulSoup(text)
    text_summary = Grammar.summary(plaintext.get_text())
    new_click = UserActions(user_id=current_user.id, action=2)
    db.session.add(new_click)
    db.session.commit()

    return render_template("summary.html", text_summary=text_summary, text_id=text_id)


@app.route("/deletetext/<text_id>", methods=["GET", "POST"])
@login_required
def deletetext(text_id):
    text = Texts.query.get_or_404(text_id)
    if text.user_id != current_user.id:
        abort(403)
    db.session.delete(text)
    db.session.commit()
    return redirect(url_for('dashboard'))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/tutorial")
def tutorial():
    return render_template("tutorial.html")


@app.route("/faq")
def faq():
    return render_template("faq.html")


