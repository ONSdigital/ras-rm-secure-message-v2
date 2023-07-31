import pytest
from sqlalchemy.exc import IntegrityError, StatementError

from secure_message_v2.controllers.messages import create_message


def test_create_message(app_with_db_session, valid_message):
    with app_with_db_session.app_context():
        message = create_message(valid_message)

        assert valid_message.items() <= message.items()
        assert message["id"] is not None


def test_create_message_no_thread(app_with_db_session, invalid_message_no_thread):
    with app_with_db_session.app_context():
        with pytest.raises(IntegrityError):
            create_message(invalid_message_no_thread)


def test_create_message_malformed(app_with_db_session, invalid_message_malformed):
    with app_with_db_session.app_context():
        with pytest.raises(StatementError):
            create_message(invalid_message_malformed)
