import os


class Config:
    """
    This object is the main configuration for the Secure Messaging Service v2.
    It contains a full default configuration
    All configuration may be overridden by setting
    the appropriate environment variable name.
    """

    SCHEME = os.getenv("http")
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = os.getenv("PORT", 5051)

    DATABASE_SCHEMA = os.getenv("DATABASE_SCHEMA", "securemessage")
    DATABASE_URI = os.getenv("DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/ras")
    JWT_SECRET = os.getenv("JWT_SECRET", "test-key")
    UAA_URL = os.getenv("UAA_URL", "http://localhost:9080")
    UAA_CHECK_ENABLED = True
    CLIENT_ID = os.getenv("CLIENT_ID", "secure_message")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET", "nearest.location.roll.change")
    THREAD_DELETION_OFFSET_IN_DAYS = 365
    SECURITY_USER_PASSWORD = os.getenv("SECURITY_USER_PASSWORD", "secret")
    SECURITY_USER_NAME = os.getenv("SECURITY_USER_NAME", "admin")
    LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO")
