import logging

from flask import Blueprint, jsonify, make_response, request
from structlog import wrap_logger
from werkzeug.exceptions import BadRequest

from secure_message_v2.controllers.messages import post_new_message
from secure_message_v2.controllers.validate import Exists, Validator

logger = wrap_logger(logging.getLogger(__name__))

messages_bp = Blueprint("messages_bp", __name__)


@messages_bp.route("/", methods=["POST"])
def post_message():
    payload = request.get_json()
    v = Validator(Exists("thread_id", "body", "is_from_internal", "sent_by"))
    if not v.validate(payload):
        logger.debug(v.errors, url=request.url)
        raise BadRequest(v.errors)
    response = post_new_message(payload)

    return make_response(jsonify(response), 201)
