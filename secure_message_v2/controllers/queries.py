from datetime import datetime

from sqlalchemy import and_
from sqlalchemy.orm import Session

from secure_message_v2.models.models import Message, Thread


def query_thread_by_id(thread_id: str, session: Session) -> Thread:
    """
    queries the Thread table filtering on thread_id
    :param thread_id: the id of the thread searching for
    :param session
    :return: the thread object
    """
    return session.query(Thread).filter_by(id=thread_id).one()


def query_message_by_id(message_id: str, session: Session) -> Message:
    """
    queries the Message table filtering on message_id
    :param message_id: the id of the message searching for
    :param session
    :return: the message object
    """
    return session.query(Message).filter_by(id=message_id).one()


def query_thread_by_filter_criteria(criteria: list, session: Session) -> list[Thread]:
    """
    queries the Thread table filtering on arguments
    :param criteria: the criteria to filter with
    :param session
    :return: a list of thread objects
    """
    return session.query(Thread).filter(and_(*criteria)).all()


def query_threads_marked_for_deletion_by_closed_at_date(date_threshold: datetime, session: Session) -> int:
    """
    Updates all threads marked_for_deletion to True if closed_at is less than date_threshold
    :param date_threshold: the upper limit date
    :param session
    :return: a count of the threads updated
    """
    return (
        session.query(Thread)
        .filter(Thread.is_closed.is_(True))
        .filter(Thread.closed_at < date_threshold)
        .update({Thread.marked_for_deletion: True})
    )


def query_delete_threads_marked_for_deletion(session: Session) -> int:
    """
    Deletes all threads marked_for_deletion
    :param session
    :return: a count of the threads updated
    """

    # ORM cascade behaviour only works for individual instances, it does not apply to “bulk” deletes as per the docs,
    # Therefore we manually have to delete the messages first

    thread_ids_to_delete = session.query(Thread.id).filter(Thread.marked_for_deletion.is_(True))
    session.query(Message).where(Message.thread_id.in_(thread_ids_to_delete)).delete()

    return session.query(Thread).where(Thread.id.in_(thread_ids_to_delete)).delete()
