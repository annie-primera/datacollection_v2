from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, TextAreaField, StringField, RadioField, IntegerField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class RegistrationForm(FlaskForm):
    gender = RadioField('Gender', validators=[DataRequired(message="This field is required")],
                        choices=[('1', 'male'), ('2', 'female'), ('3', 'non-binary'), ('4', 'other')])
    program = StringField('Programme of study', validators=[DataRequired(message="This field is required")])
    score = StringField('TOEFL/IELTS score', validators=[DataRequired(message="This field is required")])
    english = IntegerField('Approximately how many years have you studied English? (type only a number)',
                           validators=[DataRequired(message="This field is required")])
    language = StringField('What is your first language?', validators=[DataRequired(message="This field is required")])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(),
                                                     Length(min=8, message="Please choose a password of at least 8 characters")])
    password2 = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    acceptance = BooleanField('I accept', validators=[DataRequired("You need to accept the terms of the research")])
    submit = SubmitField('Register', [DataRequired()])


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
    save = SubmitField('Save')
    submit = SubmitField('Submit to instructor')

    
