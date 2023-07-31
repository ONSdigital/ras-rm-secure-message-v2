import logging

from flask import Blueprint, Response, jsonify, make_response, request
from sqlalchemy.exc import StatementError
from structlog import wrap_logger
from werkzeug.exceptions import BadRequest

from secure_message_v2.controllers.threads import create_thread
from secure_message_v2.controllers.validate import Exists, Validator

logger = wrap_logger(logging.getLogger(__name__))

threads_bp = Blueprint("threads_bp", __name__)

PAYLOAD_MALFORMED = "The thread payload is malformed"


@threads_bp.route("/", methods=["POST"])
def post_thread() -> Response:
    payload = request.get_json()
    v = Validator(Exists("subject", "category"))
    if not v.validate(payload):
        logger.error(v.errors, url=request.url)
        raise BadRequest(str(v.errors))

    try:
        response = create_thread(payload)
    except StatementError:
        logger.error(PAYLOAD_MALFORMED)
        raise BadRequest(PAYLOAD_MALFORMED)

    return make_response(jsonify(response), 201)
