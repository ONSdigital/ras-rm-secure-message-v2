from sqlalchemy.exc import StatementError

from secure_message_v2.views.threads import PAYLOAD_MALFORMED


def test_post_thread(app, valid_thread, mocker):
    thread_id = "db0471b2-c4f1-4cb2-bc50-363720286455"
    mocker.patch("secure_message_v2.views.threads.create_thread", return_value={"id": thread_id})

    with app.app_context():
        response = app.test_client().post("/threads", json=valid_thread, follow_redirects=True)

        assert thread_id.encode() in response.data
        assert 201 == response.status_code


def test_post_thread_bad_payload(app, invalid_thread_missing_key):
    with app.app_context():
        response = app.test_client().post("/threads", json=invalid_thread_missing_key, follow_redirects=True)

        assert 400 == response.status_code
        assert "Required key".encode() in response.data


def test_post_thread_statement_error(app, invalid_thread_malformed, mocker):
    mocker.patch(
        "secure_message_v2.views.threads.create_thread",
        side_effect=StatementError(message="message", params="params", statement="statement", orig=None),
    )

    with app.app_context():
        response = app.test_client().post("/threads", json=invalid_thread_malformed, follow_redirects=True)

        assert 400 == response.status_code
        assert PAYLOAD_MALFORMED.encode() in response.data
