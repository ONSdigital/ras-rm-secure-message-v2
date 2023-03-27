import logging
import os

from flask import Flask
from structlog import wrap_logger

from secure_message_v2.views.info import info_bp

logger = wrap_logger(logging.getLogger(__name__))


def create_app(config=None):
    app = Flask(__name__)
    app.name = "ras-rm-secure-message-v2"
    app_config = f"config.{config or os.getenv('APP_SETTINGS', 'Config')}"
    app.config.from_object(app_config)

    app.register_blueprint(info_bp, url_prefix="/info")

    return app
