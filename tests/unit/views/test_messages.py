from sqlalchemy.exc import IntegrityError, StatementError

from secure_message_v2.views.messages import PAYLOAD_MALFORMED, THREAD_ID_MISSING


def test_post_message(app, valid_message, mocker):
    message_id = "7eca19f4-4568-4a7d-bb2a-2ed0c64fa379"
    mock = mocker.patch("secure_message_v2.views.messages.create_message")
    mock.return_value = {"id": message_id}

    with app.app_context():
        response = app.test_client().post("/messages", json=valid_message, follow_redirects=True)

        assert 201 == response.status_code
        assert message_id.encode() in response.data


def test_post_message_bad_payload(app, invalid_message_missing_key):
    with app.app_context():
        response = app.test_client().post("/messages", json=invalid_message_missing_key, follow_redirects=True)

        assert 400 == response.status_code
        assert "Required key".encode() in response.data


def test_post_message_integrity_error(app, valid_message, mocker):
    mocker.patch(
        "secure_message_v2.views.messages.create_message",
        side_effect=IntegrityError(params="params", statement="statement", orig=None),
    )

    with app.app_context():
        response = app.test_client().post("/messages", json=valid_message, follow_redirects=True)

        assert 404 == response.status_code
        assert THREAD_ID_MISSING.encode() in response.data


def test_post_message_statement_error(app, invalid_message_malformed, mocker):
    mocker.patch(
        "secure_message_v2.views.messages.create_message",
        side_effect=StatementError(message="message", params="params", statement="statement", orig=None),
    )

    with app.app_context():
        response = app.test_client().post("/messages", json=invalid_message_malformed, follow_redirects=True)

        assert 400 == response.status_code
        assert PAYLOAD_MALFORMED.encode() in response.data
