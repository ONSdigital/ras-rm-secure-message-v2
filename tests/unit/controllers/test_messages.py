import pytest
from sqlalchemy.exc import NoResultFound, StatementError

from secure_message_v2.controllers.messages import create_message


def test_create_message(app_with_db_session, valid_message_payload):
    with app_with_db_session.app_context():
        message = create_message(valid_message_payload)

        assert valid_message_payload.items() <= message.to_response_dict().items()


def test_create_message_no_thread(app_with_db_session, invalid_message_payload_no_thread):
    with app_with_db_session.app_context():
        with pytest.raises(NoResultFound):
            create_message(invalid_message_payload_no_thread)


def test_create_message_malformed(app_with_db_session, invalid_message_payload_malformed):
    with app_with_db_session.app_context():
        with pytest.raises(StatementError):
            create_message(invalid_message_payload_malformed)
