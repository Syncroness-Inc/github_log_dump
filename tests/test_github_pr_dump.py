from unittest import TestCase
from unittest.mock import patch, MagicMock
from github_log_dump.pr_dump import pr_dump


class TestPRDump(TestCase):
    def setUp(self) -> None:
        self.repository = MagicMock()
        self.pull_1 = MagicMock()
        self.pull_1.is_merged.return_value = True
        self.pull_2 = MagicMock()
        self.pull_2.is_merged.return_value = True

        self.unmerged_pull = MagicMock()
        self.unmerged_pull.is_merged.return_value = False

        self.pulls = MagicMock()
        self.pulls.__iter__.return_value = [self.pull_1, self.pull_2, self.unmerged_pull]
        self.pulls.totalCount = len(self.pulls.__iter__.return_value)
        self.repository.get_pulls.return_value = self.pulls

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

    def test_when_pulls_are_not_merged_then_they_are_excluded_from_the_dump(self):
        # Changing "self.pull_2.is_merged()" from "True" to "False" will decrease the length of our output by one
        initial_run = pr_dump(self.repository)
        self.pull_2.is_merged.return_value = False
        second_run = pr_dump(self.repository)
        self.assertEqual(len(initial_run) - 1, len(second_run))
