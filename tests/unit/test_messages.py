import json
from unittest import TestCase
from unittest.mock import patch

from mock_alchemy.mocking import UnifiedAlchemyMagicMock

from secure_message_v2.application import create_app
from secure_message_v2.controllers.messages import post_new_message

good_payload = {
    "thread_id": "1f2324b9-b0ee-4fad-91c5-3539fd42fef7",
    "body": "Hi this is a message",
    "is_from_internal": True,
    "sent_by": "26410f78-1731-421f-a191-128833a1055c",
}
bad_payload = {"body": "Hi this is a message", "is_from_internal": True}


class TestMessages(TestCase):
    def setUp(self):
        self.app = create_app(config="TestConfig")
        self.client = self.app.test_client()

    def test_post_message_bad_payload_returns_400(self):
        # Payload is missing thread_id and sent_by
        with self.app.app_context():
            response = self.client.post("/messages", json=bad_payload, follow_redirects=True)
            self.assertEqual(400, response.status_code)

    @patch("secure_message_v2.controllers.messages.post_new_message", return_value={"id": "abcdef"})
    def test_successful_post_message_returns_201(self, mock):
        with self.app.app_context():
            self.app.db.session = UnifiedAlchemyMagicMock()
            response = self.client.post("/messages", json=good_payload, follow_redirects=True)
            response_data = json.loads(response.get_data())
            expected_result = json.dumps({"id": "abcdef"})
            self.assertEqual(201, response.status_code)
            self.assertEqual(expected_result, response_data)

    def test_message_created_when_called(self):
        with self.app.app_context():
            self.app.db.session = UnifiedAlchemyMagicMock()
            result = post_new_message(good_payload)
            self.app.db.session.add.assert_any_call()
            self.assertDictContainsSubset(result, good_payload)
            self.assertTrue("id" in result)
            self.assertTrue("sent_at" in result)
