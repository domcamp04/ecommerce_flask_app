from enum import unique

from sqlalchemy.orm import backref
from app import db, login_manager
import os
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
# from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

cart = db.Table('cart',
    db.Column('user_id', db.Integer, db.ForeignKey('user.user_id')),
    db.Column('product_id', db.Integer, db.ForeignKey('products.product_id'))
)

class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    user_cart = db.relationship('Products', secondary=cart, backref= db.backref('purchaser', lazy='dynamic'))
    

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Products(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    prod_name = db.Column(db.String(200))
    description = db.Column(db.String(300))
    price = db.Column(db.Float)
    

    def __init__(self, prod_name, description, price):
        self.prod_name=prod_name
        self.description=description
        self.price=price
        