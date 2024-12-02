import logging
from datetime import datetime, timezone

import structlog
from sqlalchemy.orm import Session

from secure_message_v2.controllers.queries import query_message_by_id
from secure_message_v2.controllers.threads import update_read_status
from secure_message_v2.models.models import Message
from secure_message_v2.utils.session_decorator import with_db_session

logger = structlog.wrap_logger(logging.getLogger(__name__))

UPDATABLE_ATTRIBUTES = ["body", "read_at"]


@with_db_session
def create_message(message_payload: dict, session: Session) -> Message:
    """
    creates a message in an existing thread
    :param message_payload: the message payload from which to create the message
    :param session
    :return: the created message object
    """

    message = Message(
        thread_id=message_payload["thread_id"],
        body=message_payload["body"],
        is_from_internal=message_payload["is_from_internal"],
        sent_by=message_payload["sent_by"],
        sent_at=datetime.now(timezone.utc),
    )
    session.add(message)
    update_read_status(message_payload["thread_id"], message.is_from_internal, not message.is_from_internal, session)

    return message


@with_db_session
def set_message_attributes(message_id: str, payload: dict, session: Session) -> Message:
    if message := query_message_by_id(message_id, session):
        for key, value in payload.items():
            if key in UPDATABLE_ATTRIBUTES:
                setattr(message, key, value)
            else:
                logger.error(f"Message attribute {key} can not be set")
                raise AttributeError
    return message


@with_db_session
def get_message_by_id(message_id: str, session: Session) -> Message:
    """
    gets the message using message_id
    :param message_id: the id of the message searching for
    :param session
    :return: the message object
    """
    return query_message_by_id(message_id, session)
