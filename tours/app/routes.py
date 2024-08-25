from flask import render_template, redirect, url_for, flash
import sqlalchemy as sa
from flask_login import logout_user, current_user, login_required, login_user

from . import app, db
from .models import Tour, User
from .forms import TourForm, RegistrationForm, LoginForm, ResetPasswordRequestForm, ResetPasswordForm
from .decorators import admin_required
from .send_mail import send_confirmation_email, send_reset_password_email


@app.route('/')
def index():
    tours = db.session.scalars(sa.select(Tour)).all()
    return render_template('index.html', tours=tours)


@app.route("/profile")
def profile():
    user_tours = db.session.scalars(current_user.user_tours.select())
    return render_template('profile.html', user_tours=user_tours)


@app.route('/tour/book/<int:tour_id>')
def book_tour(tour_id):
    tour = db.session.scalar(sa.select(Tour).where(Tour.id == tour_id))
    user_tours = db.session.scalars(current_user.user_tours.select())
    if tour in user_tours:
        return '<h1>You have already booked this tour</h1>'
    current_user.user_tours.add(tour)
    db.session.commit()
    return '<h1>You have booked this tour successfully</h1>'


@app.route('/tour/new', methods=['GET', 'POST'])
# @admin_required
def new_tour():
    form = TourForm()
    if form.validate_on_submit():
        tour = Tour(title=form.title.data, description=form.description.data,
                    country=form.country.data, price=form.price.data, time=form.time.data)
        db.session.add(tour)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('new_tour.html', form=form)


@app.route('/tour/<int:tour_id>', methods=["GET", "POST"])
# @admin_required
def edit_tour(tour_id):
    tour = db.session.scalar(sa.select(Tour).where(Tour.id == tour_id))
    form = TourForm(obj=tour)
    if form.validate_on_submit():
        tour.title = form.title.data
        tour.description = form.description.data
        tour.country = form.country.data
        tour.price = form.price.data
        tour.time = form.time.data
        db.session.commit()
        flash('You edited a tour')
        return redirect(url_for('index'))
    return render_template('new_tour.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        send_confirmation_email(user)
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/reset-password-request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.email == form.email.data))
        if user:
            send_reset_password_email(user)
    return render_template('reset_password_request.html', form=form)


@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_token(token)  # USER or None
    if not user:
        return '<h1>Invalid link'
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)


@app.route('/confirm_email/<token>')
def confirm_email(token):
    user = User.verify_token(token)
    if not user:
        return '<h1>Cannot confirm your email</h1>'
    user.is_active = True
    db.session.commit()
    return '<h1>You have confirmed your email successfully</h1>'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.email == form.email.data))
        if user is None or not user.check_password(form.password.data) or not user.is_active:
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('register'))
