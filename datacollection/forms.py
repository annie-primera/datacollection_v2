from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, TextAreaField, StringField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class RegistrationForm(FlaskForm):
    email = EmailField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired(), Length(min=8, message="Please choose a password of at least 8 characters")])
    password2 = PasswordField('password2', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('submit', [DataRequired()])


class LoginForm(FlaskForm):
    loginemail = EmailField(validators=[DataRequired(), Email()])
    loginpassword = PasswordField('password', validators=[DataRequired(message="Password field is required")])
    submit = SubmitField('submit', validators=[DataRequired()])


class NewPost(FlaskForm):
    title = StringField('Title', validators=[DataRequired(message="All texts must have a title")])
    content = TextAreaField(validators=[DataRequired()])
    submit = SubmitField('Save and check Grammar')


class EditPost(FlaskForm):
    title = StringField('Title', validators=[DataRequired(message="All texts must have a title")])
    content = TextAreaField(validators=[DataRequired()])
    submit = SubmitField('Save')
