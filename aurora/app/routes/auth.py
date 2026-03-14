"""Aurora - Authentication Routes"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models import db, User

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    return render_template('auth/login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    print(f"DEBUG: Login attempt for email: {email}")

    user = User.query.filter_by(email=email).first()

    print(f"DEBUG: User found: {user is not None}")
    if user:
        print(f"DEBUG: User email: {user.email}")
        print(f"DEBUG: Password check: {user.check_password(password)}")

    if user and user.check_password(password):
        print(f"DEBUG: Login successful, logging in user")
        login_user(user)
        flash('Välkommen tillbaka!', 'success')
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('main.index'))
    else:
        print(f"DEBUG: Login failed")
        flash('Fel e-post eller lösenord', 'danger')

    return redirect(url_for('auth.login'))

@auth.route('/register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    return render_template('auth/register.html')

@auth.route('/register', methods=['POST'])
def register_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    
    if User.query.filter_by(email=email).first():
        flash('E-post finns redan', 'danger')
        return redirect(url_for('auth.register'))
    
    user = User(email=email, name=name)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    
    flash('Konto skapat! Vänligen logga in.', 'success')
    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Du har loggats ut', 'info')
    return redirect(url_for('main.index'))
