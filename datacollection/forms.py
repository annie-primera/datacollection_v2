from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, TextAreaField, StringField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from wtf_tinymce.forms.fields import TinyMceField


class RegistrationForm(FlaskForm):
    email = EmailField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired(), Length(min=8, message="Please choose a password of at least 8 characters")])
    password2 = PasswordField('password2', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('submit', [DataRequired()])


class LoginForm(FlaskForm):
    loginemail = EmailField(validators=[DataRequired(), Email()])
    loginpassword = PasswordField('password', validators=[DataRequired(message="Password field is required")])
    submit = SubmitField('submit', validators=[DataRequired()])


class MyForm(FlaskForm):
    text = TinyMceField(
        'My WTF TinyMCE Field label',
        tinymce_options={'toolbar': 'bold italic | link | code'}
    )


class NewPost(FlaskForm):
    title = StringField('title', validators=[DataRequired(message="All texts must have a title")])
    content = TinyMceField(
        'My WTF TinyMCE Field label',
        tinymce_options={'toolbar': 'bold italic | link | code'}
    )
    submit = SubmitField('submit', validators=[DataRequired()])
