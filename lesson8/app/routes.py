from flask import render_template, redirect, url_for, request
import sqlalchemy as sa
from flask_login import logout_user, current_user, login_required, login_user

from app import app, db
from app.models import Poll, Option, Category, User


@app.route('/')
@login_required
def index():
    polls = db.session.scalars(sa.select(Poll)).all()
    categories = db.session.scalars(sa.select(Category)).all()
    return render_template('index.html', polls=polls, categories=categories)


@app.route('/poll/<int:poll_id>')
def poll(poll_id):
    poll = db.session.scalar(sa.select(Poll).where(Poll.id == poll_id))
    options = db.session.scalars(poll.options.select()).all()
    return render_template('poll.html', poll=poll, options=options)


@app.route('/option/<int:poll_id>/<int:option_id>')
def option(poll_id, option_id):
    poll = db.session.get(Poll, poll_id)
    user_polls = (db.session.scalars(current_user.voted_polls.select()).all())
    if poll in user_polls:
        return '<h1>You already voted for this poll</h1>'
    option = db.session.scalar(sa.select(Option).where(Option.id == option_id))
    option.votes += 1
    current_user.voted_polls.add(poll)
    db.session.add(option)
    db.session.commit()
    return redirect(url_for('poll', poll_id=poll_id))


@app.route('/category/<int:category_id>')
def category(category_id):
    category = db.session.scalar(sa.select(Category).where(Category.id == category_id))
    polls = db.session.scalars(category.polls.select()).all()
    return render_template('categories.html', polls=polls)


@app.route('/add-poll', methods=['GET', 'POST'])
def add_poll():
    categories = db.session.scalars(sa.select(Category)).all()
    if request.method == 'POST':
        poll_topic = request.form.get('poll_topic')
        category_id = request.form.get('category')
        category = db.session.get(Category, int(category_id))
        poll = Poll(topic=poll_topic, category=category)
        db.session.add(poll)
        db.session.commit()
        return redirect(url_for('add_option', poll_id=poll.id))
    return render_template('add_poll.html', categories=categories)


@app.route('/add-option/<int:poll_id>', methods=['GET', 'POST'])
def add_option(poll_id):
    poll = db.session.get(Poll, poll_id)
    options = db.session.scalars(poll.options.select()).all()
    if request.method == 'POST':
        title = request.form.get('title')
        option = Option(title=title, poll=poll)
        db.session.add(option)
        db.session.commit()
        return redirect(url_for('add_option', poll_id=poll_id))
    return render_template('add_option.html', poll=poll, options=options)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return '<h1>log out please</h1>'
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = db.session.scalar(sa.select(User).where(User.username == username))
        if not user or not user.check_password(password):
            return '<h1>User not valid</h1>'
        login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return '<h1>Logged out</h1>'


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return '<h1>log out please</h1>'
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect('login')
    return render_template('registration.html')


@app.route('/profile')
@login_required
def profile():
    user_polls = db.session.scalars(current_user.voted_polls.select())
    return render_template('profile.html', user_polls=user_polls)