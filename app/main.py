from flask import Flask, render_template, request, flash, url_for, redirect, session
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash

from app import app, db
from app.form import LoginForm, RegistrationForm, WithDrawForm, TransferMoneyForm, ChangePasswordForm
from app.model import User

app.config['SECRET_KEY'] = 'SjdnUends821Jsdlkvxh391ksdODnejdDw'


@app.route('/', methods=['GET'])
def index():
    session['attempt'] = 3
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    attempt = session.get('attempt')
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        if attempt == 1:
            flash('Lỗi!! Tài khoản của bạn bị khóa do nhập sai quá 3 lần')
            return redirect(url_for('login'))
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.checkPassword(form.password.data):
            attempt -= 1
            session['attempt'] = attempt
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
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
    return redirect(url_for('login'))


@app.route('/check_money')
@login_required
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


@app.route('/change_pass', methods=['POST', 'GET'])
def change_pass():
    form = ChangePasswordForm(current_user.password_hash)
    if form.validate_on_submit():
        if current_user.checkPassword(form.password_current.data):
            current_user.password_hash = generate_password_hash(form.password_new.data)
            db.session.commit()
            flash('đổi mật khẩu thành công, vui lòng đăng nhập lại')
            return redirect(url_for('logout'))
        flash(' Lỗi mật khẩu không đúng, vui lòng nhập lại')
        return redirect(url_for('change_pass'))
    return render_template('change_pass.html', form=form)


@app.route('/history', methods=['POST', 'GET'])
def check_history():
    return render_template('history_check.html')


if __name__ == '__main__':
    app.run(debug=True)
