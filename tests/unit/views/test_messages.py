from sqlalchemy.exc import NoResultFound, StatementError

from secure_message_v2.views.messages import PARENT_THREAD_NOT_FOUND, PAYLOAD_MALFORMED


def test_post_message(app, valid_message_payload, message, mocker):
    mocker.patch("secure_message_v2.views.messages.create_message", return_value=message)

    with app.app_context():
        response = app.test_client().post("/messages", json=valid_message_payload, follow_redirects=True)

        assert 201 == response.status_code


def test_post_message_bad_payload(app, invalid_message_payload_missing_key):
    with app.app_context():
        response = app.test_client().post("/messages", json=invalid_message_payload_missing_key, follow_redirects=True)

        assert 400 == response.status_code
        assert "Required key".encode() in response.data


def test_post_message_thread_no_result_error(app, valid_message_payload, mocker):
    mocker.patch(
        "secure_message_v2.views.messages.create_message",
        side_effect=NoResultFound(),
    )

    with app.app_context():
        response = app.test_client().post("/messages", json=valid_message_payload, follow_redirects=True)

        assert 400 == response.status_code
        assert PARENT_THREAD_NOT_FOUND.encode() in response.data


def test_post_message_statement_error(app, invalid_message_payload_malformed, mocker):
    mocker.patch(
        "secure_message_v2.views.messages.create_message",
        side_effect=StatementError(message="message", params="params", statement="statement", orig=None),
    )

    with app.app_context():
        response = app.test_client().post("/messages", json=invalid_message_payload_malformed, follow_redirects=True)

        assert 400 == response.status_code
        assert PAYLOAD_MALFORMED.encode() in response.data
