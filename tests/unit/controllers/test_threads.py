import uuid

import pytest
from sqlalchemy.exc import StatementError

from secure_message_v2.controllers.threads import create_thread, update_read_status
from secure_message_v2.models.models import Thread


def test_create_thread(app_with_db_session, valid_thread):
    with app_with_db_session.app_context():
        thread = create_thread(valid_thread)

        assert valid_thread.items() <= thread.items()


def test_create_thread_malformed(app_with_db_session, invalid_thread_malformed):
    with app_with_db_session.app_context():
        with pytest.raises(StatementError):
            create_thread(invalid_thread_malformed)


@pytest.mark.parametrize(
    "is_read_by_respondent, is_read_by_internal",
    [
        (True, False),
        (False, True),
    ],
)
def test_update_read_status(is_read_by_internal, is_read_by_respondent, app_with_db_session):
    uuid_thread_id = uuid.UUID("1f2324b9-b0ee-4fad-91c5-3539fd42fef7")

    with app_with_db_session.app_context():
        update_read_status(uuid_thread_id, is_read_by_internal, is_read_by_internal)
        thread = app_with_db_session.db.session.query(Thread).filter_by(id=uuid_thread_id).one()

        assert thread.is_read_by_respondent is is_read_by_internal
        assert thread.is_read_by_internal is is_read_by_internal
