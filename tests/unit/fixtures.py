import pytest

from secure_message_v2.application import create_app


@pytest.fixture(scope="class")
def app():
    app = create_app(config="TestConfig")
    app.testing = True
    return app
