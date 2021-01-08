from flask_login import UserMixin
from flask_security import RoleMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import login, db


# sử dụng cho flask-login
@login.user_loader
def load_user(id):
    return User.query.get(int(id))


roles_users_table = db.Table('roles_users',
                             db.Column('users_id', db.Integer(),
                                       db.ForeignKey('user.id')),
                             db.Column('roles_id', db.Integer(),
                                       db.ForeignKey('roles.id')))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))
    bank_number = db.Column(db.Integer)
    email = db.Column(db.String(128))
    money = db.Column(db.Float)
    active = db.Column(db.Boolean())
    roles = db.relationship('Roles', secondary=roles_users_table,
                            backref='user', lazy=True)

    def __init__(self, username, email, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def setPassword(self, password):
        self.password = password
        # mã hóa hash 256
        # self.password = generate_password_hash(password)

    def checkPassword(self, password):
        if self.password == password:
            return True
        # return False
        # mã hóa hash 256
        # return check_password_hash(self.password, password)

    def has_role(self, *args):
        return set(args).issubset({role.name for role in self.roles})


class Roles(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


if __name__ == '__main__':
    db.drop_all()
    db.create_all()
