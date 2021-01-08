from flask import Flask, url_for
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from werkzeug import security

app = Flask(__name__)
POSTGRES = {
    'user': 'postgres',
    'pw': 'postgres',
    'db': 'flaskbank',
    'host': 'localhost',
    'port': '5432',
}
app.config.update(
    DEBUG=True,
    WTF_CSRF_ENABLED=True,
    SECRET_KEY='you-will-never-guess',
    # SQLALCHEMY_DATABASE_URI='sqlite:///bank.db',
    SQLALCHEMY_DATABASE_URI='postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES,
    FILE_TYPES=['txt', 'doc', 'docx', 'odt', 'pdf', 'rtf', 'text', 'wks', 'wps', 'wpd'],
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FLASK_ADMIN_SWATCH'] = 'sandstone'
app.config['SECURITY_PASSWORD_SALT'] = 'none'
# Configure application to route to the Flask-Admin index view upon login
app.config['SECURITY_POST_LOGIN_VIEW'] = '/admin/'
# Configure application to route to the Flask-Admin index view upon logout
app.config['SECURITY_POST_LOGOUT_VIEW'] = '/admin/'
# Configure application to route to the Flask-Admin index view upon registering
app.config['SECURITY_POST_REGISTER_VIEW'] = '/admin/'
app.config['SECURITY_REGISTERABLE'] = True
# Configure application to not send an email upon registration
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False
db = SQLAlchemy(app=app)
migrate = Migrate(app, db)

# sử dụng cho @login_required
login = LoginManager(app)
login.login_view = 'login'
login.login_message = 'Lỗi!! Vui lòng đăng nhập để sử dụng dịch vụ!'
