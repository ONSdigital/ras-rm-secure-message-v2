import logging
from datetime import datetime

import structlog

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from secure_message_v2.controllers.threads import update_read_status
from secure_message_v2.models.models import Message
from secure_message_v2.utils.session_decorator import with_db_session

logger = structlog.wrap_logger(logging.getLogger(__name__))


@with_db_session
def post_new_message(posted_message: dict, session: Session):
    """
    Post a message in an existing thread
    :param posted_message: the message to be created
    :param session
    :return: the created message object
    """
    current_time = datetime.utcnow()

    message = Message(
        thread_id=posted_message["thread_id"],
        body=posted_message["body"],
        is_from_internal=posted_message["is_from_internal"],
        sent_by=posted_message["sent_by"],
        sent_at=current_time,
    )

    try:
        session.add(message)
        session.flush()
    except IntegrityError:
        raise

    update_read_status(
        message.thread_id, message.is_from_internal, not message.is_from_internal
    )

    return message.to_response_dict()
