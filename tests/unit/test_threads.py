from unittest import TestCase
from unittest.mock import patch

from mock_alchemy.mocking import UnifiedAlchemyMagicMock

from secure_message_v2.application import create_app

good_payload = {
    "subject": "Test Thread Subject",
    "category": "TEST",
}
bad_payload = {"subject": "I forgot a category"}


class TestThreads(TestCase):
    def setUp(self):
        self.app = create_app(config="TestConfig")
        self.client = self.app.test_client()

    def test_post_thread_bad_payload_returns_400(self):
        # Payload is missing category
        with self.app.app_context():
            response = self.client.post("/threads", json=bad_payload, follow_redirects=True)
            self.assertEqual(400, response.status_code)

    @patch("secure_message_v2.controllers.threads.post_new_thread", return_value={"id": "abcdef"})
    def test_successful_post_thread_returns_201(self, mock):
        with self.app.app_context():
            self.app.db.session = UnifiedAlchemyMagicMock()
            response = self.client.post("/threads", json=good_payload, follow_redirects=True)
            self.assertEqual(201, response.status_code)
