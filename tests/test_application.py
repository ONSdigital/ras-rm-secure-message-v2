import requests

from secure_message_v2.application import get_uaa_token

ACCESS_TOKEN = {
    "access_token": "a37ab9dcd1aa4a89939713c6daa87e18",
    "token_type": "bearer",
    "expires_in": 43199,
    "scope": "scim.userids scim.me scim.read",
    "jti": "a37ab9dcd1aa4a89939713c6daa87e18",
}


def test_before_request_uaa_error(app, mocker):
    mocker.patch("secure_message_v2.application.get_uaa_token", side_effect=requests.RequestException())
    app.config["UAA_CHECK_ENABLED"] = True
    response = app.test_client().get("/info/")
    app.config["UAA_CHECK_ENABLED"] = False
    assert response.status_code == 401


def test_get_uaa_token(app, requests_mock):
    requests_mock.post(f"{app.config['UAA_URL']}/oauth/token", json=ACCESS_TOKEN)
    uaa_token = get_uaa_token(app)
    assert uaa_token == ACCESS_TOKEN
