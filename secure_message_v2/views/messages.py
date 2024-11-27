import logging

from flask import Blueprint, Response, jsonify, make_response, request
from sqlalchemy.exc import NoResultFound, StatementError
from structlog import wrap_logger
from werkzeug.exceptions import BadRequest, NotFound

from secure_message_v2.authentication.authentication import jwt_authentication
from secure_message_v2.controllers.messages import (
    create_message,
    set_message_attributes,
)
from secure_message_v2.controllers.validate import Exists, Validator

logger = wrap_logger(logging.getLogger(__name__))

messages_bp = Blueprint("messages_bp", __name__)

PAYLOAD_MALFORMED = "The message payload is malformed"
PARENT_THREAD_NOT_FOUND = "The thread id in the payload does match a thread in the database"
MESSAGE_NOT_FOUND = "The message id does not match a thread in the database"


@messages_bp.route("/", methods=["POST"])
@jwt_authentication
def post_message() -> Response:
    payload = request.get_json()
    v = Validator(Exists("thread_id", "body", "is_from_internal", "sent_by"))
    if not v.validate(payload):
        logger.error(v.errors, url=request.url)
        raise BadRequest(str(v.errors))

    try:
        message = create_message(payload)
    except NoResultFound:
        logger.error(PARENT_THREAD_NOT_FOUND, thread_id=payload["thread_id"])
        raise BadRequest(PARENT_THREAD_NOT_FOUND)
    except StatementError:
        logger.error(PAYLOAD_MALFORMED, thread_id=payload["thread_id"])
        raise BadRequest(PAYLOAD_MALFORMED)

    return make_response(jsonify(message.to_response_dict()), 201)


@messages_bp.route("/<message_id>", methods=["PATCH"])
@jwt_authentication
def patch_message_by_id(message_id: str) -> Response:
    payload = request.get_json()
    try:
        message = set_message_attributes(message_id, payload)
        return make_response(jsonify(message.to_response_dict()), 200)
    except NoResultFound:
        raise NotFound(MESSAGE_NOT_FOUND)
    except AttributeError:
        return make_response("", 422)
