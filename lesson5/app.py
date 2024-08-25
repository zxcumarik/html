from flask import render_template, Flask, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'

db = SQLAlchemy(app)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=True)
    description = db.Column(db.Text)

    def __repr__(self):
        return self.name


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=True)
    content = db.Column(db.Text)
    author = db.Column(db.String(20), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)

    def __repr__(self):
        return self.title


@app.route('/posts')
def posts():
    posts_list = Post.query.all()
    return render_template('posts_list.html', posts=posts_list)


@app.route('/posts/<int:id>')
def post_by_id(id):
    post = Post.query.get_or_404(id)
    return render_template('post_detail.html', post=post)


@app.route('/posts/category/<int:category_id>')
def posts_by_category(category_id):
    posts_category = Post.query.filter_by(category_id=category_id)
    category_name = Category.query.get_or_404(category_id)
    return render_template('post_by_category.html', posts=posts_category, category=category_name)


@app.route('/posts/add', methods=['GET', 'POST'])
def posts_add():
    categories_list = Category.query.all()
    if request.method == 'POST':
        print(request.form)
        post = Post(title=request.form['title'], content=request.form['content'],
                    author=request.form['author'], category_id=int(request.form['category']))
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('posts'))
    return render_template('add_post.html', categories=categories_list)


@app.route('/categories')
def categories():
    categories_list = Category.query.all()
    return render_template('categories_list.html', categories=categories_list)


with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)