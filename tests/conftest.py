import uuid
from datetime import datetime, timezone

import pytest
from jwt import encode

from secure_message_v2.application import create_app
from secure_message_v2.models import models

THREAD_ID = uuid.UUID("1f2324b9-b0ee-4fad-91c5-3539fd42fef7")
MESSAGE_ID = uuid.UUID("e1b99ab7-001d-44d9-b23b-207becb00eaa")


@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.config["UAA_CHECK_ENABLED"] = False
    return app


@pytest.fixture(scope="session")
def jwt_payload():
    return {"party_id": "ce12b958-2a5f-44f4-a6da-861e59070a31", "role": "internal"}


@pytest.fixture(scope="session")
def test_client(app, jwt_payload):
    authorization_token = encode(jwt_payload, "test-key", algorithm="HS256", headers={"alg": "HS256", "typ": "jwt"})
    with app.test_client() as testing_client:
        testing_client.environ_base["HTTP_AUTHORIZATION"] = authorization_token
        yield testing_client


@pytest.fixture()
def valid_message_payload():
    return {
        "thread_id": THREAD_ID,
        "body": "body",
        "is_from_internal": True,
        "sent_by": uuid.UUID("26410f78-1731-421f-a191-128833a1055c"),
    }


@pytest.fixture()
def invalid_message_payload_no_thread(valid_message_payload):
    message_no_thread = valid_message_payload.copy()
    message_no_thread["thread_id"] = uuid.UUID("2f2324b9-b0ee-4fad-91c5-3539fd42fef7")
    return message_no_thread


@pytest.fixture()
def invalid_message_payload_malformed(valid_message_payload):
    message_malformed = valid_message_payload.copy()
    message_malformed["is_from_internal"] = "not bool"
    return message_malformed


@pytest.fixture()
def invalid_message_payload_missing_key(valid_message_payload):
    message_missing_key = valid_message_payload.copy()
    message_missing_key.pop("body")
    return message_missing_key


@pytest.fixture()
def valid_thread_payload():
    return {
        "subject": "subject",
        "category": "category",
        "is_closed": False,
        "closed_by_id": None,
        "closed_at": None,
        "case_id": uuid.UUID("d0a75b94-2a14-11ee-be56-0242ac120002"),
        "ru_ref": "ru_ref",
        "survey_id": uuid.UUID("d6b47eb8-2a14-11ee-be56-0242ac120002"),
        "assigned_internal_user_id": uuid.UUID("dc06fa62-2a14-11ee-be56-0242ac120002"),
        "respondent_id": uuid.UUID("eb5eb22a-2a14-11ee-be56-0242ac120002"),
        "is_read_by_respondent": False,
        "is_read_by_internal": False,
    }


@pytest.fixture()
def valid_closed_thread_payload():
    return {
        "subject": "subject",
        "category": "category",
        "is_closed": True,
        "closed_by_id": uuid.UUID("0a4b6553-3235-4120-8fd0-9876d74dddd4"),
        "closed_at": datetime.now(),
        "case_id": uuid.UUID("d0a75b94-2a14-11ee-be56-0242ac120002"),
        "ru_ref": "ru_ref",
        "survey_id": uuid.UUID("d6b47eb8-2a14-11ee-be56-0242ac120002"),
        "assigned_internal_user_id": uuid.UUID("dc06fa62-2a14-11ee-be56-0242ac120002"),
        "respondent_id": uuid.UUID("eb5eb22a-2a14-11ee-be56-0242ac120002"),
        "is_read_by_respondent": False,
        "is_read_by_internal": False,
    }


@pytest.fixture()
def valid_closed_thread_ready_for_deletion(valid_closed_thread_payload):
    ready_for_deletion = valid_closed_thread_payload.copy()
    ready_for_deletion["closed_at"] = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    return ready_for_deletion


@pytest.fixture()
def valid_marked_for_deletion(valid_closed_thread_ready_for_deletion):
    marked_for_deletion = valid_closed_thread_ready_for_deletion.copy()
    marked_for_deletion["marked_for_deletion"] = True
    return marked_for_deletion


@pytest.fixture()
def invalid_thread_payload_missing_key(valid_thread_payload):
    thread_missing_key = valid_thread_payload.copy()
    thread_missing_key.pop("category")
    return thread_missing_key


@pytest.fixture()
def invalid_thread_payload_malformed(valid_thread_payload):
    thread_malformed = valid_thread_payload.copy()
    thread_malformed["is_closed"] = "not bool"
    return thread_malformed


@pytest.fixture()
def message():
    return models.Message(
        id=MESSAGE_ID,
        thread_id=THREAD_ID,
        body="body",
        is_from_internal=True,
        sent_by="26410f78-1731-421f-a191-128833a1055c",
    )


@pytest.fixture()
def thread():
    return models.Thread(
        id=THREAD_ID,
        is_closed=False,
        is_read_by_respondent=False,
        is_read_by_internal=False,
        subject="subject",
        category="category",
        survey_id=uuid.UUID("d6b47eb8-2a14-11ee-be56-0242ac120002"),
    )


@pytest.fixture(scope="session")
def request_context(app):
    with app.test_request_context() as request_context:
        yield request_context
