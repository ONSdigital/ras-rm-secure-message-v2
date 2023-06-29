import unittest

from secure_message_v2.application import create_app


class TestMessages(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config="TestConfig")
        self.client = self.app.test_client()
        self.app.testing = True

    def test_post_message_bad_payload_returns_400(self):
        # Payload is missing thread_id and sent_by
        bad_payload = {"body": "Hi this is a message", "is_from_internal": True}
        with self.app.app_context():
            response = self.client.post("/messages", json=bad_payload)
            self.assertEqual(400, response.status_code)
