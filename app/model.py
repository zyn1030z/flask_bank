from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import login, db


# sử dụng cho flask-login
@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    bank_number = db.Column(db.Integer)
    email = db.Column(db.String(128))
    money = db.Column(db.Float)

    def __init__(self, username, email, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def setPassword(self, password):
        self.password_hash = generate_password_hash(password)

    def checkPassword(self, password):
        return check_password_hash(self.password_hash, password)


if __name__ == '__main__':
    # db.drop_all()
    db.create_all()
