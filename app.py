from flask import Flask
from flask_cors import CORS
from flask_mail import Mail

from src import register_bps

app = Flask(__name__)
CORS(app)

app.config['MAIL_SERVER']='smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = 'cde636bc04a6bc'
app.config['MAIL_PASSWORD'] = '3040e17cd10d11'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

register_bps(app, mail)
