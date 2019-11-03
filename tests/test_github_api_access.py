from unittest import TestCase
from unittest.mock import patch, MagicMock
from github_log_dump.api_access import github_login, UserPass, get_repository


class TestUserPass(TestCase):
    @patch("github_log_dump.api_access.UserPass._get_username_cmdline")
    @patch("github_log_dump.api_access.UserPass._get_password_cmdline")
    def test_new_cmdline_prompts_user_for_password_from_cmdline(self, get_password, get_username):
        get_username.return_value = "test_user"
        get_password.return_value = "testPassword"
        userpass = UserPass.new_cmdline()
        self.assertEqual(get_username.return_value, userpass.username)
        self.assertEqual(get_password.return_value, userpass.password)


class TestGetRepo(TestCase):
    def setUp(self) -> None:
        self.test_instance = MagicMock()
        self.available_repo = MagicMock
        self.available_repo.name = "available_repo"
        self.test_instance.get_user().get_repos.return_value = [self.available_repo]

    def test_if_repo_name_is_not_available_then_raises_runtime_error(self):
        repo_name = "unavailable_repo"
        with self.assertRaises(RuntimeError):
            get_repository(repo_name, self.test_instance)

    def test_if_one_repo_with_matching_name_is_found_then_return_that_object(self):
        repo = get_repository(self.available_repo.name, self.test_instance)
        self.assertIs(self.available_repo, repo)

    def test_if_multiple_repos_match_name_then_raises_runtime_error(self):
        self.test_instance.get_user().get_repos.return_value.append(self.available_repo)
        with self.assertRaises(RuntimeError):
            get_repository(self.available_repo.name, self.test_instance)


@patch('github_log_dump.api_access.Github')
class TestGithubLogin(TestCase):
    def setUp(self) -> None:
        self.test_userpass = UserPass("username", "password")
        self.test_access_token = "feedbeef"

    def test_when_no_access_token_or_userpass_is_provided_then_a_runtime_error_is_raised(self, mock_github):
        with self.assertRaises(RuntimeError):
            github_login()

    def test_when_both_and_access_token_and_userpass_is_provided_then_a_runtime_error_is_raised(self, mock_github):
        with self.assertRaises(RuntimeError):
            github_login(access_token=self.test_access_token,
                         userpass=self.test_userpass)

    def test_when_an_access_token_is_provided_then_github_attempts_to_log_in_with_provided_access_token(self, mock_github):
        instance = github_login(access_token=self.test_access_token)
        self.assertEqual(mock_github(self.test_access_token), instance)

    def test_when_userpass_is_provided_then_github_attempts_to_log_in_with_provided_userpass(self, mock_github):
        instance = github_login(userpass=self.test_userpass)
        self.assertEqual(mock_github(self.test_userpass.username, self.test_userpass.password), instance)