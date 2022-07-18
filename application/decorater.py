from functools import wraps
from json import dumps

from flask import Response
from flask_jwt_extended import verify_jwt_in_request, get_jwt


def respond(item=None, status=200):
    return Response(dumps(item), status=status)


def role(right_role):
    def inner_role(function):
        @wraps(function)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()

            return function(*args, **kwargs) if 'role' in claims and right_role == claims['role'] \
                else respond({"msg": "Missing Authorization Header"}, 401)

        return decorator

    return inner_role
