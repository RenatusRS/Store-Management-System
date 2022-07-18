from flask import Flask, request
from flask_jwt_extended import get_jwt_identity, JWTManager

from config_store import Configuration
from decorater import role, respond
from models import database, Product, Category, Order, ProductOrder

application = Flask(__name__)
application.config.from_object(Configuration)

jwt = JWTManager(application)


@application.route("/search", methods=["GET"])
@role('customer')
def search():
    product = request.args.get("name")
    category = request.args.get("category")

    products = Product.query
    categories = Category.query

    if product:
        products = products.filter(Product.name.contains(product))
        categories = categories.filter(Category.products.any(Product.name.contains(product)))

    if category:
        products = products.filter(Product.categories.any(Category.name.contains(category)))
        categories = categories.filter(Category.name.contains(category))

    return respond({
        "categories": [category.name for category in categories.all()],
        "products": [{
            "categories": [category.name for category in product.categories],
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "quantity": product.quantity
        } for product in products.all()]
    })


@application.route("/order", methods=["POST"])
@role('customer')
def order():
    requests = request.json.get("requests")
    if not requests:
        return respond({"message": "Field requests is missing."}, 400)

    fields = ['id', 'quantity']

    for num, req in enumerate(requests):

        for field in fields:
            if field not in req:
                return respond({"message": f"Product {field} is missing for request number {num}."}, 400)

        for field in fields:
            try:
                req[field] = int(req[field])
                if req[field] <= 0:
                    raise ValueError
            except ValueError:
                return respond({"message": f"Invalid product {field} for request number {num}."}, 400)

        if not Product.query.filter_by(id=req['id']).first():
            return respond({"message": f"Invalid product for request number {num}."}, 400)

    order = Order(email=get_jwt_identity())
    database.session.add(order)
    database.session.commit()

    for req in requests:
        product = Product.query.filter_by(id=req['id']).first()

        change = min(product.quantity, req['quantity'])
        product.quantity -= change

        database.session.add(ProductOrder(
            product=req['id'],
            order=order.id,
            requested=req['quantity'],
            received=change,
            price=product.price,
        ))

    database.session.commit()

    return respond({"id": order.id})


@application.route("/status", methods=["GET"])
@role('customer')
def status():
    orders = list()
    for order in Order.query.filter_by(email=get_jwt_identity()).all():
        product_orders = ProductOrder.query.filter_by(order=order.id).all()

        products = [{
            "categories": [category.name for category in product_order.prod.categories],
            "name": product_order.prod.name,
            "price": product_order.price,
            "received": product_order.received,
            "requested": product_order.requested,
        } for product_order in product_orders]

        orders.append({
            "products": products,
            "timestamp": order.timestamp.isoformat(),
            "price": sum(product["price"] * product["requested"] for product in products),
            "status": "COMPLETE" if all(
                product["requested"] == product["received"] for product in products
            ) else "PENDING"
        })

    return respond({"orders": orders})


if __name__ == "__main__":
    database.init_app(application)
    application.run(debug=True, host="0.0.0.0", port=5003)
