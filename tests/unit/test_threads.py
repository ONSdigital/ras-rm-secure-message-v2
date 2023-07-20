from mock_alchemy.mocking import UnifiedAlchemyMagicMock
from datetime import datetime
from secure_message_v2.models.models import Thread

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
            mock = mocker.patch("secure_message_v2.views.threads.post_new_thread")
            mock.return_value = {"id": "abcdef"}

            app.db.session = UnifiedAlchemyMagicMock()
            response = app.test_client().post("/threads", json=good_payload, follow_redirects=True)
            assert 201 == response.status_code

    def test_thread_to_response_dict(self):
        message = Thread(
            id = "876d0631-6e01-4871-90a4-437aca83a1c4",
            subject="Test Thread Subject",
            category="TEST",
            is_closed=False,
            closed_by_id=None,
            closed_at=None,
            case_id="90de077c-d80f-48ac-ae7e-753be9d6ac63",
            ru_ref="3febfa6d-ee1d-4943-81ff-275e9197b478",
            survey_id="1994ac5b-6dd3-4764-8ca7-792aae54f195",
            assigned_internal_user_id="9aff20e1-6a41-4b81-9979-55f306d0445f",
            respondent_id="d8ff1fe6-e482-4cc5-87fa-7949aa765f37",
            is_read_by_respondent=True,
            is_read_by_internal=False
        )

        expected = {
            "id": "876d0631-6e01-4871-90a4-437aca83a1c4",
            "subject": "Test Thread Subject",
            "category": "TEST",
            "is_closed": False,
            "closed_by_id": None,
            "closed_at": None,
            "case_id": "90de077c-d80f-48ac-ae7e-753be9d6ac63",
            "ru_ref": "3febfa6d-ee1d-4943-81ff-275e9197b478",
            "survey_id": "1994ac5b-6dd3-4764-8ca7-792aae54f195",
            "assigned_internal_user_id": "9aff20e1-6a41-4b81-9979-55f306d0445f",
            "respondent_id": "d8ff1fe6-e482-4cc5-87fa-7949aa765f37",
            "is_read_by_respondent": True,
            "is_read_by_internal": False
        }

        assert message.to_response_dict() == expected
