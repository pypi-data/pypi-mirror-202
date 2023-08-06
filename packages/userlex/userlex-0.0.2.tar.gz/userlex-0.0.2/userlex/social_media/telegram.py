import re

from userlex.social_media import SocialMedia


class Telegram(SocialMedia):
    PLATFORM_NAME = "telegram"

    USERNAME_REGEXES = [
        r"(?<!insta)(?<!gram)(?:^|\s)@(?P<username>\S+)\b",
        r'telegram:?\s+@(?P<username>\S+)\b'
    ]

    def __init__(self, username):
        self.username = username

    @property
    def url(self):
        return f"https://t.me/{self.username}"

    @staticmethod
    def from_username(username):
        return Telegram(username)

    @staticmethod
    def matches_username(username):
        return bool(Telegram.USERNAME_REGEXES.fullmatch(username))
