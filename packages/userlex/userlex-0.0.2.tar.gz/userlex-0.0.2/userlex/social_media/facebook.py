import re

from userlex.social_media import SocialMedia


class Facebook(SocialMedia):
    PLATFORM_NAME = "facebook"

    USERNAME_REGEXES = [
        r'\b(fb|facebook)\s?:\s?(?P<username>\w+)',
        r"https://www\.facebook\.com/profile\.php\?id=(?P<username>\d+)"
    ]

    def __init__(self, username):
        self.username = username

    @property
    def url(self):
        return f"https://www.facebook.com/{self.username}/"

    @staticmethod
    def from_username(username):
        return Facebook(username)

    @staticmethod
    def matches_username(username):
        return bool(Facebook.USERNAME_REGEXES.fullmatch(username))
