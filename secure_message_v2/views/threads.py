import logging

from flask import Blueprint, jsonify, make_response, request
from structlog import wrap_logger
from werkzeug.exceptions import BadRequest

from secure_message_v2.controllers.threads import post_new_thread
from secure_message_v2.controllers.validate import Exists, Validator

logger = wrap_logger(logging.getLogger(__name__))

threads_bp = Blueprint("threads_bp", __name__)


@threads_bp.route("/", methods=["POST"])
def post_thread():
    payload = request.get_json()
    v = Validator(Exists("subject", "category"))
    if not v.validate(payload):
        logger.debug(v.errors, url=request.url)
        raise BadRequest(v.errors)
    response = post_new_thread(payload)

    return make_response(jsonify(response), 201)
