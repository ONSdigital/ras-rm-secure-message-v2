from datetime import datetime

import pytest
from sqlalchemy.exc import NoResultFound, StatementError

from secure_message_v2.controllers.messages import (
    create_message,
    set_message_attributes,
)
from secure_message_v2.controllers.queries import query_message_by_id


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


def test_set_message_attributes(app_with_db_session, valid_message_payload):
    with app_with_db_session.app_context():
        message = create_message(valid_message_payload)
        date_time = datetime(2024, 1, 1, 12, 0, 0)
        updated_message = set_message_attributes(message.id, {"read_at": date_time})

        assert updated_message.read_at == date_time


def test_set_thread_invalid_attribute(app_with_db_session, valid_message_payload):
    with app_with_db_session.app_context():
        message = create_message(valid_message_payload)
        with pytest.raises(AttributeError):
            set_message_attributes(message.id, {"is_from_internal": False})

        assert query_message_by_id(message.id).is_from_internal is True
