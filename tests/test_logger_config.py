import json
import logging
from datetime import datetime, timezone

from freezegun import freeze_time
from structlog import wrap_logger

from secure_message_v2.logger_config import logger_initial_config

TIME_TO_FREEZE = datetime(2024, 1, 1, 12, 0, 0, 0, tzinfo=timezone.utc)

EXPECTED_ERROR_OUTPUT = json.dumps(
    {
        "event": "Test error",
        "severity": "error",
        "service": "secure-message-v2",
        "created_at": "2024-01-01T12:001704110400",
    }
)

EXPECTED_INFO_OUTPUT = json.dumps(
    {
        "additional_key": "additional_value",
        "event": "Test info",
        "severity": "info",
        "service": "secure-message-v2",
        "created_at": "2024-01-01T12:001704110400",
    }
)

EXPECTED_DEBUG_OUTPUT = json.dumps(
    {
        "event": "Test debug",
        "severity": "debug",
        "service": "secure-message-v2",
        "created_at": "2024-01-01T12:001704110400",
    }
)


@freeze_time(TIME_TO_FREEZE)
def test_level_debug(caplog):
    _generate_logs(caplog, "DEBUG")

    assert len(caplog.messages) == 3
    assert caplog.messages[0] == EXPECTED_ERROR_OUTPUT
    assert caplog.messages[1] == EXPECTED_INFO_OUTPUT
    assert caplog.messages[2] == EXPECTED_DEBUG_OUTPUT


@freeze_time(TIME_TO_FREEZE)
def test_level_info(caplog):
    _generate_logs(caplog, "INFO")

    assert len(caplog.messages) == 2
    assert caplog.messages[0] == EXPECTED_ERROR_OUTPUT
    assert caplog.messages[1] == EXPECTED_INFO_OUTPUT


@freeze_time(TIME_TO_FREEZE)
def test_level_error(caplog):
    _generate_logs(caplog, "ERROR")

    assert len(caplog.messages) == 1
    assert caplog.messages[0] == EXPECTED_ERROR_OUTPUT


def _generate_logs(caplog, log_level):
    caplog.set_level(log_level)
    logger_initial_config(log_level)
    logger = wrap_logger(logging.getLogger())
    logger.error("Test error")
    logger.info("Test info", additional_key="additional_value")
    logger.debug("Test debug")
