from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login
import sqlalchemy as sa
import sqlalchemy.orm as so
from typing import Optional


user_poll = sa.Table(
    'user_poll',
    db.metadata,
    sa.Column('user_id', sa.Integer, sa.ForeignKey('user.id'), primary_key=True),
    sa.Column('poll_id', sa.Integer, sa.ForeignKey('poll.id'), primary_key=True)
)


class User(UserMixin, db.Model):
    id: so.MappedColumn[int] = so.mapped_column(primary_key=True)
    username: so.MappedColumn[str] = so.mapped_column(sa.String(60))
    password_hash: so.MappedColumn[Optional[str]] = so.mapped_column(sa.String(60))
    voted_polls: so.WriteOnlyMapped['Poll'] = so.relationship('Poll', secondary=user_poll, back_populates='voters')

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
    name: so.MappedColumn[str] = so.mapped_column(sa.String(100))
    description: so.MappedColumn[str] = so.mapped_column(sa.String(100))
    polls: so.WriteOnlyMapped['Poll'] = so.relationship(back_populates='category')

    def __repr__(self):
        return f'Category: {self.name}'


class Poll(db.Model):
    id: so.MappedColumn[int] = so.mapped_column(primary_key=True)
    topic: so.MappedColumn[str] = so.mapped_column(sa.String(100))
    options: so.WriteOnlyMapped['Option'] = so.relationship(back_populates='poll')
    category_id: so.MappedColumn[int] = so.mapped_column(sa.ForeignKey(Category.id))
    category: so.Mapped[Category] = so.relationship(back_populates='polls')
    voters: so.WriteOnlyMapped[User] = so.relationship('User', secondary=user_poll, back_populates='voted_polls')

    def __repr__(self):
        return f'Poll: {self.topic}'


class Option(db.Model):
    id: so.MappedColumn[int] = so.mapped_column(primary_key=True)
    title: so.MappedColumn[str] = so.mapped_column(sa.String(100))
    votes: so.MappedColumn[int] = so.mapped_column(default=0)
    poll_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Poll.id))
    poll: so.Mapped[Poll] = so.relationship(back_populates='options')

    def __repr__(self):
        return f'Option: {self.title}'


user_tour = sa.Table(
    'user_tour',
    db.metadata,
    sa.Column('user1_id', sa.Integer, sa.ForeignKey('user1.id'), primary_key=True),
    sa.Column('tour_id', sa.Integer, sa.ForeignKey('tours.id'), primary_key=True)
)


class User1(UserMixin, db.Model):
    id: so.MappedColumn[int] = so.mapped_column(primary_key=True)
    username: so.MappedColumn[str] = so.mapped_column(sa.String(60))
    password_hash: so.MappedColumn[Optional[str]] = so.mapped_column(sa.String(60))
    voted_tours: so.WriteOnlyMapped['Tour'] = so.relationship('Tour', secondary=user_tour, back_populates='voters_tour')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return self.username


class Tour(db.Model):
    id: so.MappedColumn[int] = so.mapped_column(primary_key=True)
    title: so.MappedColumn[str] = so.mapped_column(sa.String(60))
    description: so.MappedColumn[str] = so.mapped_column(sa.String(100))
    price: so.MappedColumn[float]
    voters_tour: so.WriteOnlyMapped[User1] = so.relationship('User1', secondary=user_tour, back_populates='voted_tours')

    def __repr__(self):
        return f'Tour: {self.title}'