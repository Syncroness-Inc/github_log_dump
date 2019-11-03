from unittest import TestCase
from unittest.mock import patch
from github_log_dump import pr_dump
from github_log_dump.api_access import UserPass


@patch('github_log_dump.api_access.Github')
class TestGithubLogDump(TestCase):
    def setUp(self) -> None:
        self.test_userpass = UserPass("username", "password")
        self.test_access_token = "feedbeef"

    def test_when_no_access_token_or_userpass_is_provided_then_a_runtime_error_is_raised(self, mock_github):
        with self.assertRaises(RuntimeError):
            pr_dump()

    def test_when_both_and_access_token_and_userpass_is_provided_then_a_runtime_error_is_raised(self, mock_github):
        with self.assertRaises(RuntimeError):
            pr_dump(access_token=self.test_access_token,
                    userpass=self.test_userpass)

    def test_when_an_access_token_is_provided_then_github_attempts_to_log_in_with_provided_access_token(self, mock_github):
        pr_dump(access_token=self.test_access_token)
        mock_github.assert_called_with(self.test_access_token)

    def test_when_userpass_is_provided_then_github_attempts_to_log_in_with_provided_userpass(self, mock_github):
        pr_dump(userpass=self.test_userpass)
        mock_github.assert_called_with(self.test_userpass.username, self.test_userpass.password)
