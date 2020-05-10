from flask import render_template
from . import auth
from flask import render_template,redirect,url_for, flash,request
from flask_login import login_user,logout_user,login_required
from ..models import User
from .forms import LoginForm,RegistrationForm
from flask_login import current_user
from .. import db,bcrypt

@auth.route('/signup', methods=['POST','GET'])
def signup():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data,pass_secure=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering, you able to login now','success')
        return redirect(url_for('auth.login'))
    return render_template('admin/register.html', registration_form=form)



@auth.route('/login', methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        next = request.args.get('next')
        return redirect(next or url_for('main.index'))
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('admin/login.html', title='Login', form=form)
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('you are logout','success')
    return redirect(url_for('auth.login'))    