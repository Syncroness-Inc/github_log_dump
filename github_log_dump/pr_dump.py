"""
Dump github PR data to a dictionary
"""
from github.Repository import Repository
from github.PullRequest import PullRequest
import progressbar
from typing import List
import argparse


def _get_approved_reviews(pull: PullRequest) -> List[dict]:
    """
    Get a list of the approved reviews
    :param pull:
    :return:
    """
    return [{"username": r.user.login, "state": r.state} for r in pull.get_reviews() if r.state == "APPROVED"]


def _get_commit_hashes(pull: PullRequest) -> List[str]:
    """
    Get a list of the commit hashes associated with this PR
    :param pull:
    :return:
    """
    return [c.sha for c in pull.get_commits()]


def pr_dump(
        repository: Repository,
        progress_bar: bool = False,
        include_reviewers: bool = True,
        include_commit_hashes: bool = True) -> List[dict]:
    """
    Dump the Pull Requests for the given repository as a list of dictionaries
    :param repository:
    :param progress_bar: Include a progress bar.  Useful for commandline operation
    :param include_reviewers: Include a list of users who reviewed the PR
    :param include_commit_hashes: Include commit hashes associated with the PR
    :return:
    """
    pulls = repository.get_pulls(state="closed")

    if progress_bar:
        bar = progressbar.ProgressBar(
            maxval=pulls.totalCount,
            widgets=[progressbar.Percentage(), progressbar.Bar()]
        ).start()
        count = 0
    else:
        bar = None

    pull_entries = []

    for p in pulls:
        if p.is_merged():
            # Handle reviews here
            if include_reviewers:
                reviews = _get_approved_reviews(p)
            else:
                reviews = None
            # Handle commit hashes here
            if include_commit_hashes:
                commit_hashes = _get_commit_hashes(p)
            else:
                commit_hashes = None
            # Now create our dictionary entry
            entry = {
                "target_branch": p.base.label,
                "initiator": p.user.login,
                "merger": p.merged_by.login,
                "title": p.title,
                "number": p.number,
            }
            if reviews is not None:
                entry["reviews"] = reviews
            if commit_hashes is not None:
                entry["commits"] = commit_hashes
            pull_entries.append(entry)
        if bar:
            count += 1
            bar.update(count)

    if bar:
        bar.finish()

    return pull_entries


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dump GitHub pull request data to usable formats.")
    parser.add_argument('repo', type=str, help="Name of the repository to dump")

    args = parser.parse_args()
