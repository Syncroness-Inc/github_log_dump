from unittest import TestCase
from unittest.mock import patch, MagicMock
from github_log_dump.pr_dump import pr_dump


class TestPRDump(TestCase):
    def setUp(self) -> None:
        self.repository = MagicMock()

    @patch("progressbar.ProgressBar")
    def test_when_progress_bar_is_unset_then_progress_bar_is_not_used(self, progress_bar):
        pr_dump(self.repository, progress_bar=False)
        progress_bar.assert_not_called()

    @patch("progressbar.ProgressBar")
    def test_when_progress_bar_is_set_then_progress_bar_is_used_and_stopped(self, progress_bar):
        pr_dump(self.repository, progress_bar=True)
        progress_bar.assert_called()
        progress_bar().start.assert_called()
        progress_bar().start().finish.assert_called()
