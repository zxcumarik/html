from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from . import db
import sqlalchemy as sa
import sqlalchemy.orm as so
from typing import Optional


class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), unique=True, index=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(128), unique=True, index=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(128))
    is_admin: so.Mapped[bool] = so.mapped_column(default=False)
    user_posts: so.WriteOnlyMapped['Post'] = so.relationship(back_populates='author')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return self.username


class Category(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(100))
    description: so.Mapped[str] = so.mapped_column(sa.Text)
    posts: so.Mapped['Post'] = so.relationship(back_populates='category')

    def __repr__(self):
        return self.name


class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(100))
    body: so.Mapped[str] = so.mapped_column(sa.Text)
    time: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now())
    category_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Category.id), index=True)
    category: so.Mapped[Category] = so.relationship(back_populates='posts')
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    author: so.Mapped[User] = so.relationship(back_populates='user_posts')

    def __repr__(self):
        return self.title
