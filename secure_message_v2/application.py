import logging
import os

from flask import Flask
from sqlalchemy import DDL, create_engine, event
from sqlalchemy.orm import scoped_session, sessionmaker
from structlog import wrap_logger

from secure_message_v2.models import models
from secure_message_v2.views.info import info_bp
from secure_message_v2.views.messages import messages_bp

logger = wrap_logger(logging.getLogger(__name__))


def create_app(config=None):
    app = Flask(__name__)
    app.name = "ras-rm-secure-message-v2"
    logger.info("Creating app", name=app.name)
    app_config = f"config.{config or os.getenv('APP_SETTINGS', 'Config')}"
    app.config.from_object(app_config)

    app.register_blueprint(info_bp, url_prefix="/info")
    app.register_blueprint(messages_bp, url_prefix="/messages")

    if config == "TestConfig":
        app.testing = True
    return app


def create_database(db_connection, db_schema):
    engine = create_engine(db_connection)

    @event.listens_for(engine, "connect", insert=True)
    def set_default_schema(dbapi_connection, connection_record):
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
