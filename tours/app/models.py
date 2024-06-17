from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login
import sqlalchemy as sa
import sqlalchemy.orm as so
from typing import Optional


user_tour = sa.Table(
    'user_tour',
    db.metadata,
    sa.Column('user_id', sa.Integer, sa.ForeignKey('user.id'), primary_key=True),
    sa.Column('tour_id', sa.Integer, sa.ForeignKey('tour.id'), primary_key=True)
)


class User(UserMixin, db.Model):
    id: so.MappedColumn[int] = so.mapped_column(primary_key=True)
    username: so.MappedColumn[str] = so.mapped_column(sa.String[60])
    email: so.MappedColumn[str] = so.mapped_column(sa.String[100])
    password_hash: so.MappedColumn[Optional[str]] = so.mapped_column(sa.String[100])
    tour: so.WriteOnlyMapped['Tour'] = so.relationship('Tour', secondary=user_tour, back_populates='user')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return self.username


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))


class Tour(db.Model):
    id: so.MappedColumn[int] = so.mapped_column(primary_key=True)
    title: so.MappedColumn[str] = so.mapped_column(sa.String(100))
    description: so.MappedColumn[str]
    time: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now())
    price: so.MappedColumn[float]
    country: so.MappedColumn[str] = so.mapped_column(sa.String(100))
    user: so.WriteOnlyMapped[User] = so.relationship('User', secondary=user_tour, back_populates='tour')

    def __repr__(self):
        return f'Tour: {self.title}'
