import logging

from flask import Blueprint
from structlog import wrap_logger

from secure_message_v2.authentication.authentication import jwt_authentication
from secure_message_v2.controllers.threads import marked_for_deletion_by_closed_at_date

logger = wrap_logger(logging.getLogger(__name__))

batch_request_bp = Blueprint("batch_request_bp", __name__)


@batch_request_bp.route("/mark_thread_for_deletion", methods=["PATCH"])
@jwt_authentication
def mark_thread_for_deletion() -> tuple[str, int]:
    marked_for_deletion_by_closed_at_date()
    return "", 204
