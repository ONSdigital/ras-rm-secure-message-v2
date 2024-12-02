from sqlalchemy.exc import NoResultFound, StatementError

from secure_message_v2.views.messages import (
    MESSAGE_NOT_FOUND,
    PARENT_THREAD_NOT_FOUND,
    PAYLOAD_MALFORMED,
)


def test_post_message(test_client, valid_message_payload, message, mocker):
    mocker.patch("secure_message_v2.views.messages.create_message", return_value=message)

    response = test_client.post("/messages", json=valid_message_payload, follow_redirects=True)

    assert 201 == response.status_code


def test_post_message_bad_payload(test_client, invalid_message_payload_missing_key):
    response = test_client.post("/messages", json=invalid_message_payload_missing_key, follow_redirects=True)

    assert 400 == response.status_code
    assert "Required key".encode() in response.data


def test_post_message_thread_no_result_error(test_client, valid_message_payload, mocker):
    mocker.patch(
        "secure_message_v2.views.messages.create_message",
        side_effect=NoResultFound(),
    )

    response = test_client.post("/messages", json=valid_message_payload, follow_redirects=True)

    assert 400 == response.status_code
    assert PARENT_THREAD_NOT_FOUND.encode() in response.data


def test_post_message_statement_error(test_client, invalid_message_payload_malformed, mocker):
    mocker.patch(
        "secure_message_v2.views.messages.create_message",
        side_effect=StatementError(message="message", params="params", statement="statement", orig=None),
    )

    response = test_client.post("/messages", json=invalid_message_payload_malformed, follow_redirects=True)

    assert 400 == response.status_code
    assert PAYLOAD_MALFORMED.encode() in response.data


def test_patch_message(test_client, message, mocker):
    mocker.patch("secure_message_v2.views.messages.set_message_attributes", return_value=message)
    response = test_client.patch("/messages/e1b99ab7-001d-44d9-b23b-207becb00eaa", json={"body": "Test patch"})

    assert 200 == response.status_code
    assert str(message.id).encode() in response.data


def test_patch_thread_attribute_no_result(test_client, mocker):
    mocker.patch("secure_message_v2.views.messages.set_message_attributes", side_effect=NoResultFound())

    response = test_client.patch("/messages/aa6f09a3-1e38-4a06-b72b-4b4155197fdc", json={"is_closed": True})

    assert 404 == response.status_code
    assert MESSAGE_NOT_FOUND.encode() in response.data


def test_patch_thread_attribute_error(test_client, mocker):
    mocker.patch("secure_message_v2.views.messages.set_message_attributes", side_effect=AttributeError)
    response = test_client.patch(
        "/messages/e1b99ab7-001d-44d9-b23b-207becb00eaa", json={"id": "eb501b0b-8396-4e89-95b8-f0025fa13dec"}
    )

    assert 422 == response.status_code
