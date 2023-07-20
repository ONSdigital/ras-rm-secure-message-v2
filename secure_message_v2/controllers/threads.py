import logging

import structlog
from sqlalchemy import select
from sqlalchemy.orm import Session

from secure_message_v2.models.models import Thread
from secure_message_v2.utils.session_decorator import with_db_session

logger = structlog.wrap_logger(logging.getLogger(__name__))


@with_db_session
def post_new_thread(posted_message: dict, session: Session):
    """
    Post a new thread
    :param posted_message: the thread to be created
    :param session
    :return: the created thread object
    """

    thread = Thread(
        subject=posted_message["subject"],
        category=posted_message["category"],
        is_closed=posted_message.get("is_closed", False),
        closed_by_id=posted_message.get("closed_by_id", None),
        closed_at=posted_message.get("closed_at", None),
        case_id=posted_message.get("case_id", None),
        ru_ref=posted_message.get("ru_ref", None),
        survey_id=posted_message.get("survey_id", None),
        assigned_internal_user_id=posted_message.get("assigned_internal_user_id", None),
        respondent_id=posted_message.get("respondent_id", None),
        is_read_by_respondent=posted_message.get("is_read_by_respondent", False),
        is_read_by_internal=posted_message.get("is_read_by_internal", False),
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
    thread = session.execute(select(Thread).filter_by(id=thread_id)).scalar_one()
    thread.is_read_by_internal = internally_read
    thread.is_read_by_respondent = externally_read
    session.flush()
