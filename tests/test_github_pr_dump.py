from unittest import TestCase
from unittest.mock import patch


@patch('github_log_dump.api_access.github_login')
class TestGithubAPIAccess(TestCase):
    pass
