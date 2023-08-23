import uuid

import pytest
from sqlalchemy.exc import NoResultFound, StatementError

from secure_message_v2.controllers.threads import (
    FilterCriteriaNotImplemented,
    create_thread,
    get_thread_by_id,
    get_threads_by_args,
    update_read_status,
)
from secure_message_v2.models.models import Thread


def test_get_thread(app_with_db_session, thread):
    with app_with_db_session.app_context():
        query_result = get_thread_by_id(thread.id)

    assert query_result == thread


def test_get_thread_no_result(app_with_db_session, valid_thread_payload):
    no_result_thread_id = uuid.UUID("2ad431d9-6f41-4b24-802d-aa6a2a35717c")
    with app_with_db_session.app_context():
        with pytest.raises(NoResultFound):
            get_thread_by_id(no_result_thread_id)


def test_get_threads_by_args(app_with_db_session, thread):
    survey_id = uuid.UUID("d6b47eb8-2a14-11ee-be56-0242ac120002")
    with app_with_db_session.app_context():
        query_result = get_threads_by_args({"survey_id": survey_id})

    assert query_result == [thread]


def test_get_threads_by_args_not_implemented(app_with_db_session, thread):
    with app_with_db_session.app_context():
        with pytest.raises(FilterCriteriaNotImplemented):
            get_threads_by_args({"criteria_not_implemented": ""})


def test_create_thread(app_with_db_session, valid_thread_payload):
    with app_with_db_session.app_context():
        thread = create_thread(valid_thread_payload)

        assert {
            "subject": "subject",
            "category": "category",
            "is_closed": False,
            "closed_by_id": "0a4b6553-3235-4120-8fd0-9876d74dddd4",
            "case_id": "d0a75b94-2a14-11ee-be56-0242ac120002",
            "ru_ref": "ru_ref",
            "survey_id": "d6b47eb8-2a14-11ee-be56-0242ac120002",
            "assigned_internal_user_id": "dc06fa62-2a14-11ee-be56-0242ac120002",
            "respondent_id": "eb5eb22a-2a14-11ee-be56-0242ac120002",
            "is_read_by_respondent": False,
            "is_read_by_internal": False,
        }.items() <= thread.to_response_dict().items()


def test_create_thread_malformed(app_with_db_session, invalid_thread_payload_malformed):
    with app_with_db_session.app_context():
        with pytest.raises(StatementError):
            create_thread(invalid_thread_payload_malformed)


@pytest.mark.parametrize(
    "is_read_by_respondent, is_read_by_internal",
    [
        (True, False),
        (False, True),
    ],
)
def test_update_read_status(is_read_by_internal, is_read_by_respondent, app_with_db_session, thread):
    with app_with_db_session.app_context():
        update_read_status(thread.id, is_read_by_internal, is_read_by_internal, app_with_db_session.db.session)
        thread = app_with_db_session.db.session.query(Thread).filter_by(id=thread.id).one()

        assert thread.is_read_by_respondent is is_read_by_internal
        assert thread.is_read_by_internal is is_read_by_internal
