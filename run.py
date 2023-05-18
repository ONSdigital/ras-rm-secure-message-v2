import logging

from structlog import wrap_logger
from retrying import RetryError, retry
from sqlalchemy.exc import DatabaseError, ProgrammingError
from secure_message_v2.application import create_app, create_database

logger = wrap_logger(logging.getLogger(__name__))


def retry_if_database_error(exception):
    logger.error("Database error has occured", error=exception)
    return isinstance(exception, DatabaseError) and not isinstance(exception, ProgrammingError)


@retry(retry_on_exception=retry_if_database_error, wait_fixed=2000, stop_max_delay=30000, wrap_exception=True)
def initialise_db(app):
    app.db = create_database(app.config["DATABASE_URI"], app.config["DATABASE_SCHEMA"])


if __name__ == "__main__":
    app = create_app("Config")

    try:
        initialise_db(app)
    except RetryError:
        logger.exception("Failed to initialise database")
        exit(1)

    scheme, host, port = app.config["SCHEME"], app.config["HOST"], int(app.config["PORT"])
    app.run(debug=True, host=host, port=port)
