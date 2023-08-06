import re

from userlex.social_media import SocialMedia


class Instagram(SocialMedia):
    PLATFORM_NAME = "instagram"

    USERNAME_REGEXES = [
        r'insta(?:gram)?:?\s+@?(?P<username>\S+)\b',
        r'\big\s*:\s+@?(?P<username>\w+)\b'
    ]

    def __init__(self, username):
        self.username = username

    @property
    def url(self):
        return f"https://www.instagram.com/{self.username}/"

    @staticmethod
    def from_username(username):
        return Instagram(username)

    @staticmethod
    def matches_username(username):
        return bool(Instagram.USERNAME_REGEXES.fullmatch(username))
