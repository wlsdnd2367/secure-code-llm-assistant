import os
import unittest
from unittest.mock import patch


class GoogleAPIKeyConfigurationTests(unittest.TestCase):
    def test_missing_google_api_key_is_rejected(self):
        from security_config import MissingGoogleAPIKeyError, get_google_api_key

        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(MissingGoogleAPIKeyError):
                get_google_api_key()

    def test_google_api_key_is_read_from_environment(self):
        from security_config import get_google_api_key

        with patch.dict(
            os.environ,
            {"GOOGLE_API_KEY": "example-key-from-environment"},
            clear=True,
        ):
            self.assertEqual(
                get_google_api_key(),
                "example-key-from-environment",
            )


if __name__ == "__main__":
    unittest.main()
