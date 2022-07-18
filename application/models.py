from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()


class User(database.Model):
    __tablename__ = "users"

    id = database.Column(database.Integer, primary_key=True)

    forename = database.Column(database.String(256), nullable=False)
    surname = database.Column(database.String(256), nullable=False)
    email = database.Column(database.String(256), nullable=False, unique=True)
    password = database.Column(database.String(256), nullable=False)
    role = database.Column(database.String(256), nullable=False)


class ProductCategory(database.Model):
    __tablename__ = "product_categories"

    id = database.Column(database.Integer, primary_key=True)

    product = database.Column(database.Integer, database.ForeignKey("products.id"), nullable=False)
    category = database.Column(database.Integer, database.ForeignKey("categories.id"), nullable=False)


class ProductOrder(database.Model):
    __tablename__ = "product_orders"

    id = database.Column(database.Integer, primary_key=True)

    product = database.Column(database.Integer, database.ForeignKey("products.id"), nullable=False)
    order = database.Column(database.Integer, database.ForeignKey("orders.id"), nullable=False)

    requested = database.Column(database.Integer, nullable=False)
    received = database.Column(database.Integer, nullable=False, default=0)

    prod = database.relationship("Product", foreign_keys="ProductOrder.product")
    ord = database.relationship("Order", foreign_keys="ProductOrder.order")

    price = database.Column(database.Float, nullable=False)


class Product(database.Model):
    __tablename__ = "products"

    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(256), nullable=False)
    price = database.Column(database.Float, nullable=False)
    quantity = database.Column(database.Integer, nullable=False)

    categories = database.relationship("Category", secondary=ProductCategory.__table__, back_populates="products")
    orders = database.relationship("Order", secondary=ProductOrder.__table__, back_populates="products")


class Category(database.Model):
    __tablename__ = "categories"

    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(256), nullable=False)

    products = database.relationship("Product", secondary=ProductCategory.__table__, back_populates="categories")


class Order(database.Model):
    __tablename__ = "orders"

    id = database.Column(database.Integer, primary_key=True)

    email = database.Column(database.String(256), nullable=False)
    timestamp = database.Column(database.DateTime, nullable=False, default=datetime.now())

    products = database.relationship("Product", secondary=ProductOrder.__table__, back_populates="orders")
