from flask import Flask
from wtf_tinymce import wtf_tinymce

app = Flask(__name__)

wtf_tinymce.init_app(app)
app.secret_key = 'flkjsdfF7348503N=[F-0O3I4URasdfa7U8D54ferP4]WEOIjh45987wiehgh345ldfgn1ksyioneEkiwerRIGOQ'

from datacollection import routes