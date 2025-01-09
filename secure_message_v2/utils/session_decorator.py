import logging
from functools import wraps

import structlog
from flask import current_app
from sqlalchemy.exc import SQLAlchemyError

logger = structlog.wrap_logger(logging.getLogger(__name__))


def handle_session(f, args, kwargs):
    session = current_app.db.session()
    try:
        result = f(*args, session=session, **kwargs)
        session.commit()
        return result
    except SQLAlchemyError:
        logger.error("The session could not be committed", exc_info=True)
        session.rollback()
        raise
    finally:
        current_app.db.session.remove()


def with_db_session(f):
    """
    Wraps the supplied function, and introduces a correctly-scoped database session which is passed into the decorated
    function as the named parameter 'session'.  It handles rollbacks for you on SQLAlchemyErrors as functions with
    this wrapper are ones that modify the database.

    :param f: The function to be wrapped.
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        return handle_session(f, args, kwargs)

    return wrapper
