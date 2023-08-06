import re

from userlex.social_media import SocialMedia


class Line(SocialMedia):
    PLATFORM_NAME = "line"

    USERNAME_REGEXES = [
        r'line\s?:?\s+(?P<username>\w+)',
    ]

    def __init__(self, username):
        self.username = username

    @staticmethod
    def from_username(username):
        return Line(username)
