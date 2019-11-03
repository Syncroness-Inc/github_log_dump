"""
Dump github PR data to a dictionary
"""
from .api_access import UserPass, github_login


def pr_dump(
        access_token: str = None,
        userpass: UserPass = None,) -> dict:
    instance = github_login(access_token=access_token, userpass=userpass)
