from flask import Flask, render_template, request, flash, url_for, redirect
from flask import Flask
from flask_login import current_user, login_user, logout_user, login_required

from app import app, db
from app.form import LoginForm, RegistrationForm, WithDrawForm, TransferMoneyForm
from app.model import User

app.config['SECRET_KEY'] = 'SjdnUends821Jsdlkvxh391ksdODnejdDw'


@app.route('/index', methods=['POST', 'GET'])
def index():
    return render_template('index.html')


@app.route('/', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.checkPassword(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_check.data)
        return redirect(url_for('index'))
    return render_template('login_form.html', form=form)


@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.setPassword(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register_form.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/check_money')
def check_money():
    return render_template('check_money.html')


@app.route('/withdraw', methods=['POST', 'GET'])
def withdraw():
    form = WithDrawForm()
    if form.validate_on_submit():
        try:
            money_withdraw = int(form.money_withdraw.data)
            current_user.money = int(current_user.money) - money_withdraw
            db.session.commit()
            flash('Rút tiền thành công')
            return redirect(url_for('withdraw'))
        except:
            flash('Lỗi, Đinh dạng không đúng, vui lòng nhập lại!')
            return redirect(url_for('withdraw'))

    return render_template('withdraw.html', form=form)


@app.route('/transfer_money', methods=['POST', 'GET'])
def transfer_money():
    form = TransferMoneyForm()
    if form.validate_on_submit():
        try:
            money_transfer = int(form.money_transfer.data)
            bank_number = int(form.bank_number.data)
            user_receivered = User.query.filter_by(bank_number=bank_number).first()
            if user_receivered is not None:
                if money_transfer <= int(current_user.money):
                    current_user.money = current_user.money - money_transfer
                    user_receivered.money = int(user_receivered.money) + money_transfer
                    db.session.add(user_receivered)
                    db.session.commit()
                    flash('chuyển tiền thành công')
                    return redirect(url_for('transfer_money'))
                flash('vui lòng nhập số tiền nhỏ hơn trong tài khoản của bạn')
                return redirect(url_for('transfer_money'))
            flash('số tài khoản người nhận không đúng')
            return redirect(url_for('transfer_money'))
        except:
            flash('Lỗi, Đinh dạng không đúng, vui lòng nhập lại!')
            return redirect(url_for('transfer_money'))
    return render_template('transfer_money.html', form=form)


@app.route('/change_pass')
def change_pass():
    return render_template('change_pass.html')


if __name__ == '__main__':
    app.run()