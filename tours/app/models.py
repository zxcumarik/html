from datetime import datetime
from time import time

import jwt
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from . import db, login
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
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), unique=True, index=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(128), unique=True, index=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(128))
    is_admin: so.Mapped[bool] = so.mapped_column(default=False)
    is_active: so.Mapped[bool] = so.mapped_column(default=False, nullable=True)
    user_tours: so.WriteOnlyMapped['Tour'] = so.relationship('Tour', secondary=user_tour,
                                                             back_populates='users')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_token(self, expire_in=600):
        return jwt.encode({'token': self.id, 'exp': time() + expire_in},
                          '123456789', algorithm='HS256')

    @staticmethod
    def verify_token(token):
        try:
            id = jwt.decode(token, '123456789', algorithms=['HS256'])['token']
        except:
            return
        return User.query.get_or_404(id)

    def __repr__(self):
        return self.username


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))


class Tour(db.Model):
    id: so.MappedColumn[int] = so.mapped_column(primary_key=True)
    title: so.MappedColumn[str] = so.mapped_column(sa.String(60))
    description: so.MappedColumn[str]
    time: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now())
    price: so.MappedColumn[float]
    country: so.MappedColumn[str] = so.mapped_column(sa.String(60))
    users: so.WriteOnlyMapped[User] = so.relationship('User', secondary=user_tour, back_populates='user_tours')

    def __repr__(self):
        return f'Tour: {self.title}'
