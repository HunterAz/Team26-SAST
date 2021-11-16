from flask import Flask
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_paranoid import Paranoid

##Controllers
from website.controller.adminController import adminauth
from website.controller.adminforumController import AForum
from website.controller.userController import user
from website.controller.userforumController import userforum

##Routes
from website.routes.userrouting import userrouting
from website.routes.forumrouting import forumrouting
from website.routes.adminrouting import adminrouting
from website.routes.adminforumrouting import adminforumrouting
from .views import views

from werkzeug.datastructures import ImmutableDict
import os

##Logging
import logging

app = Flask(__name__)
paranoid = Paranoid(app)
paranoid.redirect_view = '/'

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST')
app.config['MYSQL_PORT'] = int(os.environ.get('MYSQL_PORT'))
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB')
mysql=MySQL(app)

app.register_blueprint(views,url_prefix="/")
##Routes
app.register_blueprint(userrouting, url_prefix='/')
app.register_blueprint(forumrouting, url_prefix='/')
app.register_blueprint(adminrouting, url_prefix='/')
app.register_blueprint(adminforumrouting, url_prefix='/')
##Controllers
app.register_blueprint(user,url_prefix="/")
app.register_blueprint(userforum,url_prefix="/")
app.register_blueprint(adminauth,url_prefix="/")
app.register_blueprint(AForum,url_prefix="/")

csrf = CSRFProtect()
csrf.init_app(app)

jinja_options = ImmutableDict(
    extensions=[
        'jinja2.ext.autoescape', 'jinja2.ext.with_'
])
app.jinja_env.autoescape=True

app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
)

##Logging features: changed werkzeug logging to error level
logging.basicConfig(filename='flask.log', level=logging.INFO, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

if __name__ == '__main__':
    import webbrowser
    webbrowser.open("http://127.0.0.1:5000")
    app.run(debug=True)
