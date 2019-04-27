from datetime import datetime
from datacollection import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    texts = db.relationship('Texts', backref='author', lazy=True)
    text_versions = db.relationship('TextVersions', backref='author', lazy=True)
    user_actions = db.relationship('UserActions', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.id}')"


class Texts(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}')"


class TextVersions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    text_id = db.Column(db.Integer, db.ForeignKey('texts.id'), nullable=False)

    def __repr__(self):
        return f"TextVersions('{self.id}')"


class Actions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f"Actions('{self.action}', '{self.id}')"


class UserActions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    action = db.Column(db.Integer, db.ForeignKey('actions.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"UserActions('{self.user_id}', '{self.action}')"
