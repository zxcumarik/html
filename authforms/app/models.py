from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from . import db, login
import sqlalchemy as sa
import sqlalchemy.orm as so
from typing import Optional


class User(UserMixin, db.Model):
    id: so.MappedColumn[int] = so.mapped_column(primary_key=True)
    username: so.MappedColumn[str] = so.mapped_column(sa.String(60), unique=True)
    email: so.MappedColumn[str] = so.mapped_column(sa.String(60), unique=True)
    password_hash: so.MappedColumn[Optional[str]] = so.mapped_column(sa.String(60))
    user_posts: so.WriteOnlyMapped['Post'] = so.relationship(back_populates='author')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return self.username


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))


class Category(db.Model):
    id: so.MappedColumn[int] = so.mapped_column(primary_key=True)
    name: so.MappedColumn[str] = so.mapped_column(sa.String(60))
    posts: so.WriteOnlyMapped['Post'] = so.relationship(back_populates='category')

    def __repr__(self):
        return f'{self.name}'


class Post(db.Model):
    id: so.MappedColumn[int] = so.mapped_column(primary_key=True)
    title: so.MappedColumn[str] = so.mapped_column(sa.String(60))
    content: so.MappedColumn[str] = so.mapped_column(sa.Text)
    category_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Category.id))
    category: so.Mapped[Category] = so.relationship(back_populates='posts')
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id))
    author: so.Mapped[User] = so.relationship(back_populates='user_posts')

    def __repr__(self):
        return f'{self.title}, {self.content}'
