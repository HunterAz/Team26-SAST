from flask import Flask
from flask_mail import Mail

app = Flask(__name__)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'ict3x03meok@gmail.com'
app.config['MAIL_PASSWORD'] = '3x03meOk'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEFAULT_SENDER'] = 'default_sender_email'
app.config['MAIL_ASCII_ATTACHMENTS'] = True
app.config['DEBUG'] = True
Mail(app)