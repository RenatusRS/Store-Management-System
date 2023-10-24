from re import compile, fullmatch, search

from flask import Flask, request
from flask_jwt_extended import create_access_token, jwt_required, create_refresh_token, get_jwt, \
    get_jwt_identity, JWTManager

from config_authentication import Configuration
from decorater import role, respond
from models import database, User

application = Flask(__name__)
application.config.from_object(Configuration)

jwt = JWTManager(application)

emailReg = compile(r"[^@]+@[^@]+\.[^@]{2,}")
passwordReg = compile(r"^(?=\S{8,256}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])")


@application.route("/register", methods=["POST"])
def register():
    user = dict()
    for field in ["forename", "surname", "email", "password", "isCustomer"]:
        user[field] = request.json.get(field)

        if user[field] is None or user[field] == "":
            return respond({"message": f"Field {field} is missing."}, 400)

    if not fullmatch(emailReg, user["email"]):
        return respond({"message": "Invalid email."}, 400)

    if not search(passwordReg, user["password"]):
        return respond({"message": "Invalid password."}, 400)

    if User.query.filter_by(email=user["email"]).first():
        return respond({"message": "Email already exists."}, 400)

    user["role"] = "customer" if user.pop("isCustomer") else "warehouse"

    database.session.add(User(**user))
    database.session.commit()

    return respond()


@application.route("/login", methods=["POST"])
def login():
    credentials = dict()
    for field in ["email", "password"]:
        credentials[field] = request.json.get(field, "")

        if credentials[field] == "":
            return respond({"message": f"Field {field} is missing."}, 400)

    if not fullmatch(emailReg, credentials["email"]):
        return respond({"message": "Invalid email."}, 400)

    user = User.query.filter_by(**credentials).first()

    if not user:
        return respond({"message": "Invalid credentials."}, 400)

    claims = {
        "forename": user.forename,
        "surname": user.surname,
        "role": user.role
    }

    return respond({
        "accessToken": create_access_token(identity=user.email, additional_claims=claims),
        "refreshToken": create_refresh_token(identity=user.email, additional_claims=claims)
    })


@application.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    claims = get_jwt()

    return respond({
        "accessToken": create_access_token(
            identity=get_jwt_identity(),
            additional_claims={
                "forename": claims["forename"],
                "surname": claims["surname"],
                "role": claims["role"]
            }
        )
    })


@application.route("/delete", methods=["POST"])
@role("admin")
def delete():
    email = request.json.get("email", "")

    if email == "":
        return respond({"message": "Field email is missing."}, 400)

    if not fullmatch(emailReg, email):
        return respond({"message": "Invalid email."}, 400)

    user = User.query.filter_by(email=email).first()
    if not user:
        return respond({"message": "Unknown user."}, 400)

    database.session.delete(user)
    database.session.commit()

    return respond()


if __name__ == "__main__":
    database.init_app(application)
    application.run(host="0.0.0.0", port=5002)
