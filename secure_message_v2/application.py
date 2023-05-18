import logging
import os

from flask import Flask
from structlog import wrap_logger
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from secure_message_v2.views.info import info_bp
from secure_message_v2.models import models

logger = wrap_logger(logging.getLogger(__name__))


def create_app(config=None):
    app = Flask(__name__)
    app.name = "ras-rm-secure-message-v2"
    logger.info("Creating app", name=app.name)
    app_config = f"config.{config or os.getenv('APP_SETTINGS', 'Config')}"
    app.config.from_object(app_config)

    app.register_blueprint(info_bp, url_prefix="/info")

    return app


def create_database(db_connection, db_schema):
    engine = create_engine(db_connection)
    session = scoped_session(sessionmaker())
    session.configure(bind=engine, autoflush=False, expire_on_commit=False)
    engine.session = session
    models.Base.query = session.query_property()

    logger.info("Creating database connection")

    models.Base.metadata.create_all(engine)

    return engine
