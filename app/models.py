from app import db, login_manager
import os
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
# from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

cart = db.Table('cart',
    db.Column('id', db.Integer, db.ForeignKey('user.id')),
    db.Column('product_id', db.Integer, db.ForeignKey('products.product_id'))
)

class MyCart(db.Model, UserMixin):
    cart_id = db.Column(db.Integer, primary_key=True)
    name = db.Column('name', db.String(200), db.ForeignKey('products.prod_name'))
    price = db.Column('price', db.Float, db.ForeignKey('products.price'))
    user_id = db.column('id', db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name, price, user_id):
        self.name = name
        self.price = price
        self.user_id = user_id

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    user_cart = db.relationship('Products', secondary=cart, backref= db.backref('product', lazy='dynamic'))
    

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
        