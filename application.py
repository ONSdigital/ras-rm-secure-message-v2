import logging

from flask import Flask
from flask_restful import Api
from structlog import wrap_logger

from secure_message_v2.resources.info import Info

logger = wrap_logger(logging.getLogger(__name__))

def create_app(config=None):
    app = Flask(__name__)
    app.name = "ras-rm-secure-message-v2"
    app_config = f"config.{config}"
    app.config.from_object(app_config)

    api = Api(app)
    api.add_resource(Info, "/info")

    return app