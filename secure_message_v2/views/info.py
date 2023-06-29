import logging

from flask import Blueprint, jsonify
from structlog import wrap_logger

logger = wrap_logger(logging.getLogger(__name__))

info_bp = Blueprint("info_bp", __name__)


@info_bp.route("/", methods=["GET"])
def get_info():
    info = {
        "name": "ras-rm-secure-message-v2",
    }

    return jsonify(info)
