import logging
from json import loads

from structlog import wrap_logger
from retrying import RetryError

from run import create_app, initialise_db

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
