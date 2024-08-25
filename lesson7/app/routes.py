from flask import render_template, request, redirect, url_for
import sqlalchemy as sa
from flask_login import login_user, logout_user, current_user, login_required

from app import app, db
from app.models import User


@app.route('/')
@login_required
def home():
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        user = User(name=name, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        user = db.session.scalar(sa.select(User).where(User.name == name))
        if not user or not user.check_password(password):
            return '<h1>User not valid</h1>'
        login_user(user)
        return redirect(url_for('home'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return render_template('signup.html')
