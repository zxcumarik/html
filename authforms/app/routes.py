from flask import render_template, redirect, url_for, request
import sqlalchemy as sa
from flask_login import logout_user, current_user, login_required, login_user
from .forms import RegistrationForm, LoginForm, CategoryForm, PostForm
from . import app, db
from .models import User, Category, Post


@app.route('/')
@app.route("/home")
def home():
    return render_template('index.html')


@app.route("/profile")
def profile():
    return render_template('profile.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/posts')
def posts():
    posts = db.session.scalars(sa.select(Post))
    return render_template('posts.html', posts=posts)


@app.route('/category')
def category():
    categories = db.session.scalars(sa.select(Category))
    return render_template('categories.html', categories=categories)


@app.route('/category/<int:category_id>')
def category_posts(category_id):
    category = db.session.scalar(sa.select(Category).where(Category.id == category_id))
    posts_list = db.session.scalars(category.posts.select())
    return render_template('posts.html', posts=posts_list)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.email == form.email.data))
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('home'))
    return render_template('login.html', form=form)


@app.route('/category/new', methods=['POST', 'GET'])
def new_category():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(name=form.name.data)
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('create_category.html', form=form)


@app.route('/post/new', methods=['POST', 'GET'])
def new_post():
    form = PostForm()
    form.category.choices = [(category.id, category.name) for category in Category.query.all()]
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, category_id=form.category.data,
                    author=current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('create_post.html', form=form)


@app.route('/post/<int:post_id>', methods=['POST', 'GET'])
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostForm()
    form.category.choices = [(category.id, category.name) for category in Category.query.all()]
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.category_id = form.content.data
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.category.data = post.category_id
    return render_template('create_post.html', form=form)