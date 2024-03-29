import logging

from retrying import RetryError
from structlog import wrap_logger

from run import initialise_db
from secure_message_v2.application import create_app

"""
This is a duplicate of run.py, with minor modifications to support gunicorn execution
"""

logger = wrap_logger(logging.getLogger(__name__))

app = create_app()

logger.debug("Created Flask app.")

try:
    initialise_db(app)
except RetryError:
    logger.exception("Failed to initialise database")
    exit(1)

scheme, host, port = app.config["SCHEME"], app.config["HOST"], int(app.config["PORT"])
