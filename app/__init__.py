import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

app = Flask(__name__)
bootstrap = Bootstrap(app=app)
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
db = SQLAlchemy(app=app)

# sử dụng cho @login_required
login = LoginManager(app)
login.login_view = 'login'
login.login_message = 'Lỗi!! Vui lòng đăng nhập để sử dụng dịch vụ!'
