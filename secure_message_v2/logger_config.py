import logging
import sys

import structlog


def logger_initial_config(log_level: str = "INFO") -> None:
    def add_severity_level(_, method_name: str, event_dict: dict) -> dict:
        """
        Adds the log level to the event dict.
        """
        event_dict["severity"] = method_name
        return event_dict

    def add_service(_, __, event_dict: dict) -> dict:
        """
        Adds the service name (secure-message-v2) to the event dict.
        """
        event_dict["service"] = "secure-message-v2"
        return event_dict

    logging.basicConfig(format="%(message)s", stream=sys.stdout, level=logging.INFO)

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            add_severity_level,  # type: ignore
            add_service,  # type: ignore
            structlog.processors.format_exc_info,
            structlog.processors.TimeStamper(fmt="%Y-%m-%dT%H:%M%s", utc=True, key="created_at"),
            structlog.processors.JSONRenderer(indent=None),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.getLevelName(log_level)),
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
