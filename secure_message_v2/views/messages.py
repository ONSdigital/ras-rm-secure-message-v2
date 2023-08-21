import logging

from flask import Blueprint, Response, jsonify, make_response, request
from sqlalchemy.exc import IntegrityError, StatementError
from structlog import wrap_logger
from werkzeug.exceptions import BadRequest, NotFound

from secure_message_v2.controllers.messages import create_message
from secure_message_v2.controllers.validate import Exists, Validator

logger = wrap_logger(logging.getLogger(__name__))

messages_bp = Blueprint("messages_bp", __name__)

PAYLOAD_MALFORMED = "The message payload is malformed"
THREAD_ID_MISSING = "The specified Thread does not exist in the database"


@messages_bp.route("/", methods=["POST"])
def post_message() -> Response:
    payload = request.get_json()
    v = Validator(Exists("thread_id", "sent_by"))
    if not v.validate(payload):
        logger.error(v.errors, url=request.url)
        raise BadRequest(str(v.errors))

    try:
        response = create_message(payload)
    except IntegrityError as e:
        logger.error(e.params, thread_id=payload["thread_id"])
        raise NotFound(THREAD_ID_MISSING)
    except StatementError:
        logger.error(PAYLOAD_MALFORMED, thread_id=payload["thread_id"])
        raise BadRequest(PAYLOAD_MALFORMED)

    return make_response(jsonify(response), 201)
