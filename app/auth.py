from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import *
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    global admin,user
    color="blue"
    text = "none"
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        Role= request.form.get('Role')

        if Role =='Admin':
            user = Admin.query.filter_by(email=email).first()
            if user:
                if (user.password, password):
                    flash('Logged in successfully!')
                    login_user(user, remember=True)
                    return redirect(url_for('view.admin'))
                else:
                    flash('Incorrect password, try again.')
            else:
                flash('Email does not exist.')

        elif Role =='User':
            user = User.query.filter_by(email=email).first()
            if user:
                if check_password_hash(user.password, password):
                    flash('Logged in successfully!')
                    login_user(user, remember=True)
                    return redirect(url_for('view.index'))
                else:
                    flash('Incorrect password, try again.')
            else:
                flash('Email does not exist.')

    return render_template("login.html", user=current_user,color=color,text=text)


@auth.route('/logout')
@login_required
def logout():
    flash('logged out. login again?')
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    color="blue"
    text = "none"
    if request.method == 'POST':
        email = request.form.get('email')
        Full_Name = request.form.get('Full_Name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, name=Full_Name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('view.index'))

    return render_template("register.html", user=current_user,color=color,text=text)