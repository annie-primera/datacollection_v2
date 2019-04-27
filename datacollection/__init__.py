from flask import Flask
from wtf_tinymce import wtf_tinymce
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

wtf_tinymce.init_app(app)
app.secret_key = 'flkjsdfF7348503N=[F-0O3I4URasdfa7U8D54ferP4]WEOIjh45987wiehgh345ldfgn1ksyioneEkiwerRIGOQ'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db?check_same_thread=False'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from datacollection import routes
