"""
github_log_dump - a command line tool for pulling logs from github repositories

See attached README.md file for usage
Copyright: Syncroness, INC - 2019
"""
from github import Github


class UserPass:
    """
    Represents a username and password
    """
    def __init__(self, username: str, password: str):
        """
        Create a new UserPass
        :param username:
        :param password:
        """
        self.username = username
        self.password = password


def github_log_dump(
        access_token: str = None,
        userpass: UserPass = None,) -> None:
    if (access_token is not None) == (userpass is not None):
        raise RuntimeError("Exactly one of access_token and userpass parameters must be defined")
    if access_token is not None:
        instance = Github(access_token)
    else:
        instance = Github(userpass.username, userpass.password)


def cmdline():
    """
    Command line entry point for the github_log_dump program.
    :return:
    """
    pass
