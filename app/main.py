from flask import Flask, render_template, request, flash, url_for, redirect, session
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, login_user, logout_user, login_required
from flask_security import SQLAlchemyUserDatastore, Security
from werkzeug.security import generate_password_hash

from app import app, db
from app.form import LoginForm, RegistrationForm, WithDrawForm, TransferMoneyForm, ChangePasswordForm
from app.model import User, Roles
from flask_admin import Admin
from flask_admin import helpers as admin_helpers


@app.template_filter()
def currencyFormat(value):
    value = float(value)
    return "{:,.0f} VND".format(value)


@app.route('/', methods=['GET'])
def index():
    session['attempt'] = 3
    return render_template('index.html')


@app.route('/login_user', methods=['POST', 'GET'])
def login():
    attempt = session.get('attempt')
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if attempt == 1:
            user.active = False
            db.session.commit()
            flash('Lỗi!! Tài khoản của bạn bị khóa do nhập sai quá 3 lần')
            return redirect(url_for('login'))
        if user is None:
            attempt -= 1
            session['attempt'] = attempt
            flash('Lỗi!! Thông tin tài khoản không đúng')
            return redirect(url_for('login'))
        elif not user.checkPassword(form.password.data):
            attempt -= 1
            session['attempt'] = attempt
            flash('Lỗi!! Thông tin tài khoản không đúng')
            return redirect(url_for('login'))
        login_user(user)
        print(current_user.has_role('role_user'))
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
@login_required
def withdraw():
    form = WithDrawForm()
    if form.validate_on_submit():
        try:
            money_withdraw = int(form.money_withdraw.data)
            if money_withdraw > int(current_user.money):
                flash('Lỗi!! Vui lòng nhập số tiền nhỏ hơn trong tài khoản hiện có')
                return redirect(url_for('withdraw'))
            current_user.money = int(current_user.money) - money_withdraw
            db.session.commit()
            flash('Rút tiền thành công')
            return redirect(url_for('withdraw'))
        except:
            flash('Lỗi, Đinh dạng không đúng, vui lòng nhập lại!')
            return redirect(url_for('withdraw'))

    return render_template('withdraw.html', form=form)


@app.route('/transfer_money', methods=['POST', 'GET'])
@login_required
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
                    flash('Chuyển tiền thành công')
                    return redirect(url_for('transfer_money'))
                flash('vui lòng nhập số tiền nhỏ hơn trong tài khoản của bạn')
                return redirect(url_for('transfer_money'))
            flash('Lỗi!!Số tài khoản người nhận không đúng')
            return redirect(url_for('transfer_money'))
        except:
            flash('Lỗi!!Đinh dạng không đúng, vui lòng nhập lại!')
            return redirect(url_for('transfer_money'))
    return render_template('transfer_money.html', form=form)


@app.route('/change_pass', methods=['POST', 'GET'])
@login_required
def change_pass():
    form = ChangePasswordForm(current_user.password)
    if form.validate_on_submit():
        if current_user.checkPassword(form.password_current.data):
            # current_user.password = generate_password_hash(form.password_new.data)
            current_user.password = form.password_new.data
            db.session.commit()
            flash('đổi mật khẩu thành công, vui lòng đăng nhập lại')
            return redirect(url_for('logout'))
        flash(' Lỗi mật khẩu không đúng, vui lòng nhập lại')
        return redirect(url_for('change_pass'))
    return render_template('change_pass.html', form=form)


@app.route('/history', methods=['POST', 'GET'])
@login_required
def check_history():
    return render_template('history_check.html')


user_datastore = SQLAlchemyUserDatastore(db, User, Roles)
security = Security(app, user_datastore)
admin = Admin(app, name='Admin', base_template='my_master.html', template_mode='bootstrap3')


class MyModelView(ModelView):
    # def is_accessible(self):
    #     return (current_user.is_active and
    #             current_user.is_authenticated)
    can_export = True

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        if current_user.has_role('role_admin'):
            self.can_create = True
            self.can_edit = True
            self.can_delete = True
            # self.can_export = True
            return True
        return False

    def _handle_view(self, name):
        if not self.is_accessible():
            return redirect(url_for('security.login'))

    column_list = ['username', 'password', 'bank_number', 'email', 'money', 'active', 'roles']


class MyModelViewRoles(ModelView):
    # def is_accessible(self):
    #     return (current_user.is_active and
    #             current_user.is_authenticated)
    can_export = True

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        if current_user.has_role('role_admin'):
            self.can_create = True
            self.can_edit = True
            self.can_delete = True
            # self.can_export = True
            return True
        return False

    def _handle_view(self, name):
        if not self.is_accessible():
            return redirect(url_for('security.login'))

    column_list = ['id', 'name', 'description']


admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelViewRoles(Roles, db.session))


@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        get_url=url_for,
        h=admin_helpers
    )


if __name__ == '__main__':
    app.run(debug=True)
