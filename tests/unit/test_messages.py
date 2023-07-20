from mock_alchemy.mocking import UnifiedAlchemyMagicMock

good_payload = {
    "thread_id": "1f2324b9-b0ee-4fad-91c5-3539fd42fef7",
    "body": "Hi this is a good message",
    "is_from_internal": True,
    "sent_by": "26410f78-1731-421f-a191-128833a1055c",
}
bad_payload = {"body": "Hi this is a message", "is_from_internal": True}


class TestMessages:
    def test_post_message_bad_payload_returns_400(self, app):
        # Payload is missing thread_id and sent_by
        with app.app_context():
            response = app.test_client().post("/messages", json=bad_payload, follow_redirects=True)
            assert 400 == response.status_code

    def test_successful_post_message_returns_201(self, app, mocker):
        with app.app_context():
            mock = mocker.patch("secure_message_v2.views.messages.post_new_message")
            mock.return_value = {"id": "abcdef"}

            app.db.session = UnifiedAlchemyMagicMock()
            response = app.test_client().post("/messages", json=good_payload, follow_redirects=True)
            assert 201 == response.status_code
