import logging
from datetime import datetime

import structlog
from utils.session_decorator import with_db_session

from secure_message_v2.models.models import Message

logger = structlog.wrap_logger(logging.getLogger(__name__))


@with_db_session
def post_new_message(message, session):
    """
    Post a message in an existing thread
    :param message: the message to be created
    :param session
    :return: the created message object
    """

    message = Message(
        thread_id=message["thread_id"],
        body=message["body"],
        is_from_internal=message["is_from_internal"],
        sent_by=message["sent_by"],
    )
    message["sent_at"] = datetime.utcnow

    session.add(message)

    return message.to_response_dict()
