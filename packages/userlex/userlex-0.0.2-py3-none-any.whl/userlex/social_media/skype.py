import re

from userlex.social_media import SocialMedia


class Skype(SocialMedia):
    PLATFORM_NAME = "skype"

    USERNAME_REGEXES = [
        r'(?P<username>(live)?:\.cid\.\w+)',  # live:.cid.xxx
        r'skype\s+(?P<username>\w+\d+)\b'
    ]

    def __init__(self, username):
        if ':' in username:
            # ensure "live:" prefix for new usernames
            username = 'live:' + username.split(':')[-1]
        self.username = username

    @property
    def url(self):
        # return link to this Skype user
        return f"skype:{self.username}?chat"

    @staticmethod
    def from_username(username):
        return Skype(username)

    @staticmethod
    def matches_username(username):
        return bool(Skype.USERNAME_REGEX.fullmatch(username))
