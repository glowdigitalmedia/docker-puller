import unittest
from mock import patch
import app

class DockerPullerTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.app.test_client()
        config_dict = {
                "host": "localhost",
                "port": 8000,
                "token": "abc123",
                "hooks": {
                    "hello": "scripts/hello.sh"
                }
            }
        app.config = config_dict

    @patch('subprocess.call')
    def test_valid_token_and_hook(self, subprocess_call):
        response = self.app.post("/?token=abc123&hook=hello")
        self.assertEqual(response.status_code, 200)
        subprocess_call.assert_called_once_with("scripts/hello.sh")

    def test_invalid_token(self):
        response = self.app.post("/?token=abc123456&hook=hello")
        self.assertEqual(response.status_code, 400)
        assert "Invalid token" in response.data

    def test_get_not_allowed(self):
        response = self.app.get("/?token=abc123&hook=hello")
        self.assertEqual(response.status_code, 405)

    def test_invalid_hook(self):
        response = self.app.post("/?token=abc123&hook=wronghook")
        self.assertEqual(response.status_code, 404)
        assert "Hook not found" in response.data

    def test_hook_not_specified(self):
        response = self.app.post("/?token=abc123")
        self.assertEqual(response.status_code, 400)
        assert "missing hook" in response.data

if __name__ == '__main__':
    unittest.main()
