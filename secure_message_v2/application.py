import logging

import requests
from flask import Flask, jsonify
from requests.exceptions import ConnectionError, Timeout
from sqlalchemy import DDL, create_engine, event
from sqlalchemy.orm import scoped_session, sessionmaker
from structlog import wrap_logger
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed

from secure_message_v2.authentication.authentication import JWTValidationError
from secure_message_v2.models import models
from secure_message_v2.views.info import info_bp
from secure_message_v2.views.messages import messages_bp
from secure_message_v2.views.threads import threads_bp

logger = wrap_logger(logging.getLogger(__name__))


class UAAError(Exception):
    def __init__(self, message):
        self.message = message


def create_app():
    app = Flask(__name__)
    app.name = "ras-rm-secure-message-v2"
    logger.info("Creating app", name=app.name)
    app_config = "config.Config"
    app.config.from_object(app_config)

    app.register_blueprint(info_bp, url_prefix="/info")
    app.register_blueprint(messages_bp, url_prefix="/messages")
    app.register_blueprint(threads_bp, url_prefix="/threads")

    @app.errorhandler(UAAError)
    @app.errorhandler(JWTValidationError)
    def handle_exception(e):
        logger.error(e.message)
        response = jsonify({"error": "Unauthorized"})
        response.status_code = 401
        return response

    @app.before_request
    def before_request():
        if app.config["UAA_CHECK_ENABLED"]:
            try:
                get_uaa_token(app)
            except requests.RequestException:
                raise UAAError("unable to obtain UAA token")

    return app


def create_database(db_connection, db_schema):  # pragma: no cover
    engine = create_engine(db_connection)

    @event.listens_for(engine, "connect", insert=True)
    def set_default_schema(dbapi_connection, _):
        existing_autocommit = dbapi_connection.autocommit
        dbapi_connection.autocommit = True
        cursor = dbapi_connection.cursor()
        cursor.execute("SET SESSION search_path='%s'" % db_schema)
        cursor.close()
        dbapi_connection.autocommit = existing_autocommit

    session = scoped_session(sessionmaker())
    session.configure(bind=engine, autoflush=False, expire_on_commit=False)
    engine.session = session
    models.Base.query = session.query_property()

    logger.info("Creating database connection")

    event.listen(models.Base.metadata, "before_create", DDL(f"CREATE SCHEMA IF NOT EXISTS {db_schema}"))
    models.Base.metadata.create_all(engine)

    return engine


@retry(
    stop=stop_after_attempt(10),
    wait=wait_fixed(10),
    retry=retry_if_exception_type(ConnectionError) | retry_if_exception_type(Timeout),
)
def get_uaa_token(app):
    headers = {"Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json"}
    payload = {"grant_type": "client_credentials", "response_type": "token", "token_format": "opaque"}
    uaa_token = requests.post(
        f"{app.config['UAA_URL']}/oauth/token",
        headers=headers,
        params=payload,
        auth=(app.config["CLIENT_ID"], app.config["CLIENT_SECRET"]),
    )
    return uaa_token.json()
