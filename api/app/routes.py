from flask_restful import Api, Resource, reqparse
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

from app import db
from flask import jsonify
from .models import Category, Post, User


def initialize_routes(api: Api):
    api.add_resource(UserRegisterResource, '/register')
    api.add_resource(CategoryListResource, '/categories')
    api.add_resource(CategoryResource, '/categories/<int:id>')
    api.add_resource(PostListResource, '/posts')
    api.add_resource(PostResource, '/posts/<int:id>')


class UserRegisterResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, help='Username cannot be blank')
        parser.add_argument('email', required=True, help='Email cannot be blank')
        parser.add_argument('password', required=True, help='Password cannot be blank')
        args = parser.parse_args()
        hashed_password = generate_password_hash(args['password'])
        new_user = User(username=args['username'], email=args['email'], password_hash=hashed_password)
        db.session.add(new_user)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return {'message': 'User already exists'}
        return {'message': 'User created successfully'}


class CategoryListResource(Resource):
    def get(self):
        categories = db.session.query(Category).all()
        return [{'id': cat.id, 'name': cat.name} for cat in categories]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, help='Name cannot be blank')
        parser.add_argument('description', required=True, help='Description cannot be blank')

        args = parser.parse_args()
        category = Category(name=args['name'], description=args['description'])
        db.session.add(category)
        db.session.commit()
        return {'id': category.id, 'name': category.name}, 201


class CategoryResource(Resource):
    def get(self, id):
        category = db.session.query(Category).get_or_404(id)
        return {'id': category.id, 'name': category.name}

    def put(self, id):
        category = db.session.query(Category).get_or_404(id)
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, help='Name cannot be blank')
        parser.add_argument('description', required=True, help='Description cannot be blank')
        args = parser.parse_args()

        category.name = args['name']
        category.description = args['description']
        db.session.commit()
        return {'id': category.id, 'name': category.name}

    def delete(self):
        category = db.session.query(Category).all
        pass


class PostListResource(Resource):
    def get(self):
        posts = db.session.query(Post).all()
        return [{'id': p.id, 'title': p.title, 'content': p.body, 'time': p.time, 'category id': p.category_id} for p in
                posts]


class PostResource(Resource):
    def get(self, id):
        post = db.session.query(Post).get_or_404(id)
        return {'id': post.id, 'name': post.title}

    def put(self, id):
        post = db.session.query(Post).get_or_404(id)
        parser = reqparse.RequestParser()
        parser.add_argument('title', required=True, help='Name cannot be blank')
        parser.add_argument('body', required=True, help='Description cannot be blank')
        args = parser.parse_args()

        post.title = args['title']
        post.body = args['body']
        db.session.commit()
        return {'id': post.id, 'name': post.title}
