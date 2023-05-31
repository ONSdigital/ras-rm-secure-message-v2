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
    DATABASE_URI = os.getenv("DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres")


class TestConfig(Config):
    """
    Put test-specific config here
    """
