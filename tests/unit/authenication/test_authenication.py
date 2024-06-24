import pytest
from jwt import encode

from secure_message_v2.authentication.authentication import (
    JWTValidationError,
    jwt_authentication,
)


def test_authentication(app, jwt_payload, request_context):
    _add_authorization_header(jwt_payload, request_context)
    assert "authenticated" == _mock_decorator()


def test_missing_role(app, request_context):
    jwt_payload = {"party_id": "ce12b958-2a5f-44f4-a6da-861e59070a31"}
    _add_authorization_header(jwt_payload, request_context)

    with pytest.raises(JWTValidationError) as e:
        _mock_decorator()

    assert e.value.message == "JWT claims missing role"


def test_missing_party_id(app, request_context):
    jwt_payload = {"role": "internal"}
    _add_authorization_header(jwt_payload, request_context)

    with pytest.raises(JWTValidationError) as e:
        _mock_decorator()
    assert e.value.message == "JWT claims missing party_id"


def test_incorrect_key(app, jwt_payload, request_context):
    _add_authorization_header(jwt_payload, request_context, "incorrect-key")

    with pytest.raises(JWTValidationError) as e:
        _mock_decorator()
    assert e.value.message == "The JWT token could not be decoded"


def test_missing_authorization_header(app):
    with app.test_request_context():
        with pytest.raises(JWTValidationError) as e:
            _mock_decorator()
    assert e.value.message == "Authorization header is missing"


def _add_authorization_header(payload, flask_context, key="test-key"):
    authorization_token = encode(payload, key, algorithm="HS256", headers={"alg": "HS256", "typ": "jwt"})
    flask_context.request.headers = {"Authorization": authorization_token}


def _mock_decorator():
    @jwt_authentication
    def decorator():
        return "authenticated"

    return decorator()
