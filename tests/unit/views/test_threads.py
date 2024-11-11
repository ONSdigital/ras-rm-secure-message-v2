from sqlalchemy.exc import NoResultFound, StatementError

from secure_message_v2.controllers.threads import FilterCriteriaNotImplemented
from secure_message_v2.views.threads import PAYLOAD_MALFORMED, THREAD_NOT_FOUND


def test_get_thread(test_client, thread, mocker):
    mocker.patch("secure_message_v2.views.threads.get_thread_by_id", return_value=thread)

    response = test_client.get(f"/threads/{thread.id}", follow_redirects=True)

    assert str(thread.id).encode() in response.data
    assert 200 == response.status_code


def test_get_thread_no_result(test_client, mocker):
    mocker.patch("secure_message_v2.views.threads.get_thread_by_id", side_effect=NoResultFound())
    not_found_thread_id = "db0471b2-c4f1-4cb2-bc50-363720286455"

    response = test_client.get(f"/threads/{not_found_thread_id}", follow_redirects=True)

    assert 404 == response.status_code
    assert THREAD_NOT_FOUND.encode() in response.data


def test_get_threads_by_args(test_client, thread, mocker):
    mocker.patch("secure_message_v2.views.threads.get_threads_by_args", return_value=[thread])
    survey_id = "1f2324b9-b0ee-4fad-91c5-3539fd42fef7"

    response = test_client.get(f"/threads?survey_id={survey_id}", follow_redirects=True)

    assert str(thread.id).encode() in response.data
    assert 200 == response.status_code


def test_get_threads_by_args_no_results(test_client, mocker):
    mocker.patch("secure_message_v2.views.threads.get_threads_by_args", return_value=[])
    no_threads_survey_id = "e5296b1a-f115-4bcc-944d-1796d6102fe0"

    response = test_client.get(f"threads?survey_id={no_threads_survey_id}", follow_redirects=True)

    assert 200 == response.status_code
    assert [] == response.json


def test_get_threads_by_args_filter_criteria_not_implemented(test_client, mocker):
    mocker.patch(
        "secure_message_v2.views.threads.get_threads_by_args",
        side_effect=FilterCriteriaNotImplemented("Filter criteria not implemented"),
    )

    response = test_client.get("threads?not_implemented=", follow_redirects=True)

    assert 400 == response.status_code
    assert "Filter criteria not implemented".encode() in response.data


def test_post_thread(test_client, valid_thread_payload, thread, mocker):
    mocker.patch("secure_message_v2.views.threads.create_thread", return_value=thread)

    response = test_client.post("/threads", json=valid_thread_payload, follow_redirects=True)

    assert str(thread.id).encode() in response.data
    assert 201 == response.status_code


def test_post_thread_unauthorized(app, valid_thread_payload, thread, mocker):
    mocker.patch("secure_message_v2.views.threads.create_thread", return_value=thread)
    response = app.test_client().post("/threads", json=valid_thread_payload, follow_redirects=True)

    assert "Unauthorized".encode() in response.data
    assert 401 == response.status_code


def test_post_thread_bad_payload(test_client, invalid_thread_payload_missing_key):
    response = test_client.post("/threads", json=invalid_thread_payload_missing_key, follow_redirects=True)

    assert 400 == response.status_code
    assert "Required key".encode() in response.data


def test_post_thread_statement_error(test_client, invalid_thread_payload_malformed, mocker):
    mocker.patch(
        "secure_message_v2.views.threads.create_thread",
        side_effect=StatementError(message="message", params="params", statement="statement", orig=None),
    )
    response = test_client.post("/threads", json=invalid_thread_payload_malformed, follow_redirects=True)

    assert 400 == response.status_code
    assert PAYLOAD_MALFORMED.encode() in response.data


def test_patch_thread(test_client, thread, mocker):
    mocker.patch("secure_message_v2.views.threads.set_thread_attributes", return_value=thread)
    response = test_client.patch("/threads/3144aba6-baf0-4b72-8fa3-90badc431a82", json={"is_closed": True})

    assert 200 == response.status_code
    assert str(thread.id).encode() in response.data


def test_patch_thread_attribute_no_result(test_client, mocker):
    mocker.patch("secure_message_v2.views.threads.set_thread_attributes", side_effect=NoResultFound())

    response = test_client.patch("/threads/aa6f09a3-1e38-4a06-b72b-4b4155197fdc", json={"is_closed": True})

    assert 404 == response.status_code
    assert THREAD_NOT_FOUND.encode() in response.data


def test_patch_thread_attribute_error(test_client, mocker):
    mocker.patch("secure_message_v2.views.threads.set_thread_attributes", side_effect=AttributeError)
    response = test_client.patch(
        "/threads/3144aba6-baf0-4b72-8fa3-90badc431a82", json={"survey_id": "eb501b0b-8396-4e89-95b8-f0025fa13dec"}
    )

    assert 422 == response.status_code
