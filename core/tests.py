import json
from django.test import TestCase

from core.gh_webhook_handling import verify_secret, generate_signature


class GHWebhookTestCase(TestCase):
    def setUp(self):
        self.secret = "UwU"
        self.payload = {
            "sender": {"login": "test_user"},
            "action": "opened",
            "pull_request": {"merged": False},
            "issue": {"state_reason": "completed"},
        }
        self.payload_bytes = json.dumps(self.payload).encode("utf-8")
        self.signature = generate_signature(self.secret, self.payload_bytes)

    def test_valid_signature(self):
        self.assertTrue(verify_secret(self.secret, self.payload_bytes, self.signature))

    def test_invalid_signature(self):
        wrong_signature = "silly:3"
        self.assertFalse(
            verify_secret(self.secret, self.payload_bytes, wrong_signature)
        )
