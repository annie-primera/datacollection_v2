from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import ProWritingAidSDK

app = Flask(__name__)

app.secret_key = ''
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db?check_same_thread=False'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

configuration = ProWritingAidSDK.Configuration()
configuration.host = 'https://api.prowritingaid.com'
configuration.api_key['licenseCode'] = ''

from datacollection import routes
