import logging

import structlog

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
        is_closed=message["is_closed"] or False,
        closed_by_id=message["closed_by_id"] or None,
        closed_at=message["closed_at"] or None,
        case_id=message["case_id"] or None,
        ru_ref=message["ru_ref"] or None,
        survey_id=message["survey_id"] or None,
        assigned_internal_user_id=message["assigned_internal_user_id"] or None,
        respondent_id=message["respondent_id"] or None,
        is_read_by_respondent=message["is_read_by_respondent"] or False,
        is_read_by_internal=message["is_read_by_internal"] or False,
        # We default to unread for both of these, as posting the message after will set the flags properly
    )

    session.add(thread)

    return thread.to_response_dict()
