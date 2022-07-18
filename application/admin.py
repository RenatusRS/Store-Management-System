from flask import Flask
from flask_jwt_extended import JWTManager

from config_store import Configuration
from decorater import role, respond
from models import database, ProductOrder, Category

application = Flask(__name__)
application.config.from_object(Configuration)

jwt = JWTManager(application)


@application.route("/productStatistics", methods=["GET"])
@role('admin')
def productStatistics():
    statistics = dict()
    for product_order in ProductOrder.query.filter(ProductOrder.requested > 0).all():
        if product_order.prod.name not in statistics:
            statistics[product_order.prod.name] = {
                "name": product_order.prod.name,
                "sold": 0,
                "waiting": 0
            }

        statistics[product_order.prod.name]["sold"] += product_order.requested
        statistics[product_order.prod.name]["waiting"] += product_order.requested - product_order.received

    return respond({"statistics": list(statistics.values())})


@application.route("/categoryStatistics", methods=["GET"])
@role('admin')
def categoryStatistics():
    statistics = dict()
    for category in Category.query.all():
        statistics[category.name] = 0

    for product_order in ProductOrder.query.all():
        for category in product_order.prod.categories:
            statistics[category.name] += product_order.requested

    statistics = sorted(statistics.items(), key=lambda x: (-x[1], x[0]))

    return respond({"statistics": [statistic[0] for statistic in statistics]})


if __name__ == "__main__":
    database.init_app(application)
    application.run(debug=True, host="0.0.0.0", port=5001)
