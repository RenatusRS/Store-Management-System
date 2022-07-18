from csv import reader
from io import StringIO
from json import dumps

from flask import Flask, request
from flask_jwt_extended import JWTManager
from redis.client import Redis

from config_store import Configuration
from decorater import role, respond
from models import database

application = Flask(__name__)
application.config.from_object(Configuration)

jwt = JWTManager(application)


@application.route("/update", methods=["POST"])
@role('warehouse')
def update():
    if "file" not in request.files:
        return respond({"message": "Field file is missing."}, 400)

    products = []
    for line, fields in enumerate(reader(StringIO(request.files['file'].stream.read().decode('utf-8')))):
        if len(fields) != 4:
            return respond({"message": f"Incorrect number of values on line {line}."}, 400)

        try:
            if int(fields[2]) <= 0:
                raise ValueError()
        except ValueError:
            return respond({"message": f"Incorrect quantity on line {line}."}, 400)

        try:
            if float(fields[3]) <= 0:
                raise ValueError()
        except ValueError:
            return respond({"message": f"Incorrect price on line {line}."}, 400)

        products.append(fields)

    with Redis(Configuration.REDIS) as redis:
        redis.rpush("products", dumps(products))

    return respond()


if __name__ == "__main__":
    database.init_app(application)
    application.run(debug=True, host="0.0.0.0", port=5004)
