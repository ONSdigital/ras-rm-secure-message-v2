import requests

from secure_message_v2.application import get_uaa_token


def test_before_request_uaa_error(app, mocker):
    mocker.patch("secure_message_v2.application.get_uaa_token", side_effect=requests.RequestException())
    app.config["UAA_CHECK_ENABLED"] = True
    response = app.test_client().get("/info/")
    app.config["UAA_CHECK_ENABLED"] = False
    assert response.status_code == 401


def test_get_uaa_token(app, requests_mock):
    requests_mock.post(f"{app.config['UAA_URL']}/oauth/token", json={"name": "awesome-mock"})
    uaa_token = get_uaa_token(app)
    assert uaa_token == {"name": "awesome-mock"}
