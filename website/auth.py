from flask import Blueprint, render_template, request, flash, url_for, redirect
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint("auth", __name__)

@auth.route("/login", methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in sucessful!', category = 'success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect Password, please try again!', category = 'error')
        else:
            flash('Email does not exisit!', category = 'error')

    
    return render_template("login.html", user = current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route("/sign-up", methods = ['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email address already registered', category='error')
        elif len(email) < 4:
            flash('Email address must be greater than 4 characters', category='error')
        elif len(firstName) < 2:
            flash('First name must be greater than 2 characters', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match', category='error')
        elif len(password1) < 8:
            flash('Password must be greater than 8 characters', category='error')
        else:
            hashed_password = generate_password_hash(password1, method='pbkdf2:sha256')
            new_user = User(email=email, first_name=firstName, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)

            flash('Account created', category='success')
            return redirect(url_for('views.home'))
        
    return render_template("signup.html", user=current_user)
