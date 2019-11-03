"""
Access to the Github API
"""
from github import Github
from github.Repository import Repository
from getpass import getpass


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

    @staticmethod
    def _get_username_cmdline():
        return input("Github Username: ")

    @staticmethod
    def _get_password_cmdline():
        return getpass()

    @classmethod
    def new_cmdline(cls) -> 'UserPass':
        """
        Create a new instance of a "UserPass" object by prompting the user from the command line
        :return:
        """
        return cls(cls._get_username_cmdline(), cls._get_password_cmdline())


def github_login(
        access_token: str = None,
        userpass: UserPass = None,) -> Github():
    # Handle access_token and userpass input, create Github instance
    if (access_token is not None) == (userpass is not None):
        raise RuntimeError("Exactly one of access_token and userpass parameters must be defined")
    if access_token is not None:
        instance = Github(access_token)
    else:
        instance = Github(userpass.username, userpass.password)
    return instance


def get_repository(name: str, github_instance: Github) -> Repository:
    """
    Returns a matching Repository object based on the string, or raises a RuntimeError
    if no match can be found
    :param name:
    :param github_instance:
    :return:
    """
    matching_repos = [repo for repo in github_instance.get_user().get_repos() if repo.name == name]
    if len(matching_repos) == 0:
        raise RuntimeError(f"Cannot find a repository matching name '{name}'")
    if len(matching_repos) > 1:
        raise RuntimeError(f"Found too many repositories matching name '{name}'")
    return matching_repos[0]
