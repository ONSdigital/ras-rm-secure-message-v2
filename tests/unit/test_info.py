import unittest

from application import create_app


class TestInfo(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config="TestConfig")
        self.app.testing = True

    def test_info_with_git_info(self):
        response = self.app.get("/info")

        self.assertEqual(response.status_code, 200)
        self.assertIn('"name": "ras-rm-secure-message-v2"'.encode(), response.data)  # noqa: E501
