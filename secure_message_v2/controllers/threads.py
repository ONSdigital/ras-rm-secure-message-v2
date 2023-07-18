import logging

import structlog
from sqlalchemy import select

from secure_message_v2.models.models import Thread
from secure_message_v2.utils.session_decorator import with_db_session

logger = structlog.wrap_logger(logging.getLogger(__name__))


@with_db_session
def post_new_thread(message, session):
    """
    Post a new thread
    :param message: the thread to be created
    :param session
    :return: the created thread object
    """

    thread = Thread(
        subject=message["subject"],
        category=message["category"],
        is_closed=message.get("is_closed", False),
        closed_by_id=message.get("closed_by_id", None),
        closed_at=message.get("closed_at", None),
        case_id=message.get("case_id", None),
        ru_ref=message.get("ru_ref", None),
        survey_id=message.get("survey_id", None),
        assigned_internal_user_id=message.get("assigned_internal_user_id", None),
        respondent_id=message.get("respondent_id", None),
        is_read_by_respondent=message.get("is_read_by_respondent", False),
        is_read_by_internal=message.get("is_read_by_internal", False),
        # We default to unread for both of these, as posting the message after will set the flags properly
    )

    session.add(thread)
    session.flush()

    return thread.to_response_dict()


@with_db_session
def update_read_status(thread_id, internally_read, externally_read, session):
    """
    Update the read status of a thread
    :param thread_id: the UUID of the thread to be updated
    :param internally_read: a boolean of whether it has been read internally
    :param externally_read: a boolean of whether it has been read externally
    :param session
    """
    thread = session.execute(select(Thread).filter_by(thread_id=thread_id)).scalar_one()
    thread.is_read_by_internal = internally_read
    thread.is_read_by_respondent = externally_read
    session.flush()
