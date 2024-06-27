import logging

from flask import Blueprint, Response, jsonify, make_response, request
from sqlalchemy.exc import NoResultFound, StatementError
from structlog import wrap_logger
from werkzeug.exceptions import BadRequest, NotFound

from secure_message_v2.authentication.authentication import jwt_authentication
from secure_message_v2.controllers.threads import (
    FilterCriteriaNotImplemented,
    create_thread,
    get_thread_by_id,
    get_threads_by_args,
)
from secure_message_v2.controllers.validate import Exists, Validator

logger = wrap_logger(logging.getLogger(__name__))

threads_bp = Blueprint("threads_bp", __name__)

PAYLOAD_MALFORMED = "The thread payload is malformed"
THREAD_NOT_FOUND = "The thread id does not match a thread in the database"


@threads_bp.route("/<thread_id>/", methods=["GET"])
@jwt_authentication
def get_thread(thread_id: str) -> Response:
    try:
        thread = get_thread_by_id(thread_id)
    except NoResultFound:
        raise NotFound(THREAD_NOT_FOUND)

    return make_response(jsonify(thread.to_response_dict()), 200)


@threads_bp.route("/", methods=["GET"])
@jwt_authentication
def get_threads_by_request_args() -> Response:
    try:
        threads = get_threads_by_args(request.args)
    except FilterCriteriaNotImplemented as e:
        raise BadRequest(e.error_message)

    response_data = []
    for thread in threads:
        response_data.append(thread.to_response_dict())

    return make_response(response_data, 200)


@threads_bp.route("/", methods=["POST"])
@jwt_authentication
def post_thread() -> Response:
    payload = request.get_json()
    v = Validator(Exists("subject", "category"))
    if not v.validate(payload):
        logger.error(v.errors, url=request.url)
        raise BadRequest(str(v.errors))

    try:
        thread = create_thread(payload)
    except StatementError:
        logger.error(PAYLOAD_MALFORMED)
        raise BadRequest(PAYLOAD_MALFORMED)

    return make_response(jsonify(thread.to_response_dict()), 201)
