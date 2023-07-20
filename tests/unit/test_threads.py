import pytest
from mock_alchemy.mocking import UnifiedAlchemyMagicMock

from secure_message_v2.application import create_app

good_payload = {
    "subject": "Test Thread Subject",
    "category": "TEST",
}
bad_payload = {"subject": "I forgot a category"}


class TestThreads:
    def test_post_thread_bad_payload_returns_400(self, app):
        # Payload is missing category
        with app.app_context():
            response = app.test_client().post("/threads", json=bad_payload, follow_redirects=True)
            assert 400 == response.status_code

    def test_successful_post_thread_returns_201(self, app, mocker):
        with app.app_context():
            mock = mocker.patch("secure_message_v2.views.threads")
            mock.post_new_thread.return_value = {"id": "abcdef"}

            app.db.session = UnifiedAlchemyMagicMock()
            response = app.test_client().post("/threads", json=good_payload, follow_redirects=True)
            assert 201 == response.status_code
