from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import ProWritingAidSDK

app = Flask(__name__)

app.secret_key = 'flkjsdfF7348503NF0O3I4URasdfa7U8D54ferP4]WEOIjh45987wiehgh345ldfgn1ksyioneEkiwerRIGOQ'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://wwwgrammaraidedu_ahibert:Sqlpr9.dl4eNaq@localhost/wwwgrammaraidedu_datacollection'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = '',
    MAIL_PASSWORD = '',
))
mail = Mail(app)

configuration = ProWritingAidSDK.Configuration()
configuration.host = 'https://api.prowritingaid.com'
configuration.api_key['licenseCode'] = 'A17D00BF-3DF2-40DA-AE0F-0B8172F2CB1C'

from datacollection import routes

