import logging
from datetime import datetime, timedelta, timezone

import structlog
from flask import current_app as app
from sqlalchemy.orm import Session

from secure_message_v2.controllers.queries import (
    query_delete_threads_marked_for_deletion,
    query_thread_by_filter_criteria,
    query_thread_by_id,
    query_threads_marked_for_deletion_by_closed_at_date,
)
from secure_message_v2.models.models import Thread
from secure_message_v2.utils.session_decorator import with_db_session

logger = structlog.wrap_logger(logging.getLogger(__name__))

UPDATABLE_ATTRIBUTES = ["is_closed", "closed_by_id", "closed_at"]


class FilterCriteriaNotImplemented(Exception):
    def __init__(self, error_message: str) -> None:
        self.error_message = error_message


@with_db_session
def get_thread_by_id(thread_id: str, session: Session) -> Thread:
    """
    gets the thread using thread_id
    :param thread_id: the id of the thread searching for
    :param session
    :return: the thread object
    """
    return query_thread_by_id(thread_id, session)


@with_db_session
def get_threads_by_args(args: dict, session: Session) -> list[Thread]:
    """
    gets threads using a key/value dict of arguments
    :param args: the arguments to searching for
    :param session
    :return: list of thread objects
    """

    criteria = []
    for key, value in args.items():
        if key == "survey_id":
            criteria.append(Thread.survey_id == value)
        else:
            logger.error(f"invalid argument {key} used to filter Thread")
            raise FilterCriteriaNotImplemented(f"You can not filter on {key}")

    return query_thread_by_filter_criteria(criteria, session)


@with_db_session
def create_thread(thread_payload: dict, session: Session) -> Thread:
    """
    creates a new thread
    :param thread_payload: the thread payload from which to create the thread
    :param session
    :return: the created thread object
    """
    logger.info(f"thread_payload {thread_payload}")

    thread = Thread(
        subject=thread_payload["subject"],
        category=thread_payload["category"],
        is_closed=thread_payload.get("is_closed", False),
        closed_by_id=thread_payload.get("closed_by_id"),
        closed_at=thread_payload.get("closed_at"),
        case_id=thread_payload.get("case_id"),
        ru_ref=thread_payload.get("ru_ref"),
        survey_id=thread_payload.get("survey_id"),
        assigned_internal_user_id=thread_payload.get("assigned_internal_user_id"),
        respondent_id=thread_payload.get("respondent_id"),
        is_read_by_respondent=thread_payload.get("is_read_by_respondent", False),
        is_read_by_internal=thread_payload.get("is_read_by_internal", False),
        marked_for_deletion=thread_payload.get("marked_for_deletion", False),
        # We default to unread for both of these, as posting the message after will set the flags properly
    )

    session.add(thread)
    return thread


def update_read_status(thread_id: str, internally_read: bool, externally_read: bool, session: Session) -> None:
    """
    Update the read status of a thread
    :param thread_id: the UUID of the thread to be updated
    :param internally_read: a boolean of whether it has been read internally
    :param externally_read: a boolean of whether it has been read externally
    :param session
    """

    thread = query_thread_by_id(thread_id, session)
    thread.is_read_by_internal = internally_read
    thread.is_read_by_respondent = externally_read


@with_db_session
def marked_for_deletion_by_closed_at_date(session: Session) -> None:
    """
    Updates all threads marked_for_deletion to True if closed_at_date is less than a configurable date
    :param session
    """
    date_threshold = datetime.now(timezone.utc) - timedelta(days=app.config["THREAD_DELETION_OFFSET_IN_DAYS"])
    threads_updated = query_threads_marked_for_deletion_by_closed_at_date(date_threshold, session)
    logger.info(f"{threads_updated} Threads marked for deletion")


@with_db_session
def set_thread_attributes(thread_id: str, payload: dict, session: Session) -> Thread:
    if thread := query_thread_by_id(thread_id, session):
        for key, value in payload.items():
            if key in UPDATABLE_ATTRIBUTES:
                setattr(thread, key, value)
            else:
                logger.error(f"Thread attribute {key} can not be set")
                raise AttributeError
    return thread


@with_db_session
def delete_threads_marked_for_deletion(session: Session) -> None:
    """
    Deletes all threads marked_for_deletion
    :param session
    """
    threads_updated = query_delete_threads_marked_for_deletion(session)
    logger.info(f"{threads_updated} Threads deleted")
