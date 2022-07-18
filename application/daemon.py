from json import loads

from flask import Flask
from redis.client import Redis

from config_store import Configuration
from models import database, Product, Category, ProductOrder, Order

application = Flask(__name__)
application.config.from_object(Configuration)


def insert(passed):
    categories = list()
    for category in passed[0].split("|"):
        database_category = Category.query.filter(Category.name == category).first()

        if database_category is None:
            database_category = Category(name=category)
            database.session.add(database_category)

        categories.append(database_category)

    database.session.add(
        Product(
            name=passed[1],
            quantity=int(passed[2]),
            price=float(passed[3]),
            categories=categories
        )
    )


def update(existing, passed):
    categories = passed[0].split("|")

    for category in existing.categories:
        if category.name not in categories:
            return

    passed_quantity = int(passed[2])
    passed_price = float(passed[3])

    existing.price = (existing.quantity * existing.price + passed_quantity * passed_price) / (
            existing.quantity + passed_quantity)

    existing.quantity += passed_quantity

    for order_request in sorted(
            [order_request for order_request in ProductOrder.query.filter_by(product=existing.id).all()],
            key=lambda x: x.ord.timestamp):

        change = min(existing.quantity, order_request.requested - order_request.received)

        order_request.received += change
        existing.quantity -= change

        if existing.quantity == 0:
            break


if __name__ == '__main__':
    database.init_app(application)

    with Redis(Configuration.REDIS) as redis:
        while True:
            with application.app_context():
                for product in loads(redis.blpop("products")[1].decode()):
                    database_product = Product.query.filter_by(name=product[1]).first()
                    insert(product) if database_product is None else update(database_product, product)

                database.session.commit()
