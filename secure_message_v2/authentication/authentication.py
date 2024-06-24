from functools import wraps

from flask import current_app, request
from jwt import decode
from jwt.exceptions import DecodeError


class JWTValidationError(Exception):
    def __init__(self, message):
        self.message = message


def jwt_authentication(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if not (token := request.headers.get("Authorization")):
            raise JWTValidationError("Authorization header is missing")

        jwt_key = current_app.config["JWT_KEY"]
        try:
            claims = decode(token, jwt_key, algorithms="HS256")
        except DecodeError:
            raise JWTValidationError("The JWT token could not be decoded")

        if not claims.get("party_id"):
            raise JWTValidationError("JWT claims missing party_id")
        if not claims.get("role"):
            raise JWTValidationError("JWT claims missing role")

        return f(*args, **kwargs)

    return decorator
