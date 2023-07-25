import logging
from datetime import datetime
from typing import Optional, Union
from uuid import UUID

import structlog
from sqlalchemy.orm import Session

from secure_message_v2.controllers.threads import update_read_status
from secure_message_v2.models.models import Message
from secure_message_v2.utils.session_decorator import with_db_session

logger = structlog.wrap_logger(logging.getLogger(__name__))


@with_db_session
def create_message(message_payload: dict, session: Session) -> dict[str, Optional[Union[UUID, str, bool, datetime]]]:
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
        sent_at=datetime.utcnow(),
    )
    session.add(message)
    session.flush()
    update_read_status(message.thread_id, message.is_from_internal, not message.is_from_internal)

    return message.to_response_dict()
