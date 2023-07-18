import logging
from datetime import datetime

import structlog

from secure_message_v2.controllers.threads import update_read_status
from secure_message_v2.models.models import Message
from secure_message_v2.utils.session_decorator import with_db_session

logger = structlog.wrap_logger(logging.getLogger(__name__))


@with_db_session
def post_new_message(message, session):
    """
    Post a message in an existing thread
    :param message: the message to be created
    :param session
    :return: the created message object
    """
    current_time = datetime.utcnow()

    message = Message(
        thread_id=message["thread_id"],
        body=message["body"],
        is_from_internal=message["is_from_internal"],
        sent_by=message["sent_by"],
        sent_at=current_time,
    )

    created_message = session.add(message)

    print(vars(created_message))

    update_read_status(
        created_message["thread_id"], created_message["is_from_internal"], not created_message["is_from_internal"]
    )

    return created_message.to_response_dict()
