from unittest import TestCase
from unittest.mock import patch
from github_log_dump import github_log_dump, UserPass


@patch('github_log_dump.Github')
class TestGithubLogDump(TestCase):
    def setUp(self) -> None:
        self.test_userpass = UserPass("username", "password")
        self.test_api_key = "feedbeef"

    def test_when_no_api_key_or_userpass_is_provided_then_a_runtime_error_is_raised(self, mock_github):
        with self.assertRaises(RuntimeError):
            github_log_dump()

    def test_when_both_and_api_key_and_userpass_is_provided_then_a_runtime_error_is_raised(self, mock_github):
        with self.assertRaises(RuntimeError):
            github_log_dump(api_key=self.test_api_key,
                            userpass=self.test_userpass)
