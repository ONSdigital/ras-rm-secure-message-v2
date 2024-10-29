import logging
from typing import Optional

from flask import Blueprint, current_app
from flask_httpauth import HTTPBasicAuth
from structlog import wrap_logger

from secure_message_v2.controllers.threads import (
    delete_threads_marked_for_deletion,
    marked_for_deletion_by_closed_at_date,
)

logger = wrap_logger(logging.getLogger(__name__))

batch_request_bp = Blueprint("batch_request_bp", __name__)
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username: str, password: str) -> Optional[str]:
    if (
        username == current_app.config["SECURITY_USER_NAME"]
        and password == current_app.config["SECURITY_USER_PASSWORD"]
    ):
        return username


@batch_request_bp.route("/mark_threads_for_deletion", methods=["PATCH"])
@auth.login_required
def mark_threads_for_deletion() -> tuple[str, int]:
    marked_for_deletion_by_closed_at_date()
    return "", 204


@batch_request_bp.route("/threads", methods=["DELETE"])
@auth.login_required
def delete_threads() -> tuple[str, int]:
    delete_threads_marked_for_deletion()
    return "", 204
