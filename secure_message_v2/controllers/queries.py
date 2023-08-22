from sqlalchemy import and_
from sqlalchemy.orm import Session

from secure_message_v2.models.models import Thread


def query_thread_by_id(thread_id: str, session: Session) -> Thread:
    """
    queries the Thread table filtering on thread_id
    :param thread_id: the id of the thread searching for
    :param session
    :return: the thread object
    """
    return session.query(Thread).filter_by(id=thread_id).one()


def query_thread_by_filter_criteria(criteria: list, session: Session) -> list[Thread]:
    """
    queries the Thread table filtering on arguments
    :param criteria: the criteria to filter with
    :param session
    :return: a list of thread objects
    """
    return session.query(Thread).filter(and_(*criteria)).all()
