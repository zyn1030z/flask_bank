from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, FloatField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from werkzeug.security import generate_password_hash
from flask_bootstrap import Bootstrap

from app.model import User


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_check = BooleanField('Remember check')
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=self.username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=self.email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class WithDrawForm(FlaskForm):
    money_withdraw = StringField('Rút tiền', validators=[DataRequired()])
    submit = SubmitField('Register')


class TransferMoneyForm(FlaskForm):
    money_transfer = StringField('Số tiền cần chuyển', validators=[DataRequired()])
    bank_number = StringField('Số tài khoản người nhận', validators=[DataRequired()])
    submit = SubmitField('Chuyển tiền')
    #
    # def validate_money_transfer(self, email):
    #     user = User.query.filter_by(email=self.email.data).first()
    #     if user is not None:
    #         raise ValidationError('Please use a different email address.')


class ChangePasswordForm(FlaskForm):
    password_current = StringField('Current Password', validators=[DataRequired()])
    password_new = StringField('New Password', validators=[DataRequired()])
    submit = SubmitField('Change')

    def __init__(self, password_database, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.password_database = password_database

    def validate_password(self, password_current):
        user = User.query.filter_by(password_hash=generate_password_hash(self.password_current.data)).first()
        if user is not None:
            raise ValidationError('Please retype password.')
