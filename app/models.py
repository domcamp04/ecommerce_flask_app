from enum import unique
from app import db, login_manager
import os
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
# from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    product = db.relationship('Products', backref='author', lazy=True)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prod_name = db.Column(db.String(200))
    description = db.Column(db.String(300))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, prod_name, description, user_id):
        self.prod_name=prod_name
        self.description=description
        self.user_id=user_id