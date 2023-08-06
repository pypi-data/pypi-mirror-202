import re
import unicodedata
from typing import List


class SocialMedia:
    PLATFORMS = {}
    PLATFORM_NAME = None
    USERNAME_CASE_SENSITIVE = False

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        SocialMedia.PLATFORMS[cls.PLATFORM_NAME] = cls

    @staticmethod
    def from_username(username):
        # create a new instance of the child class
        raise NotImplementedError

    @staticmethod
    def matches_username(username):
        raise NotImplementedError

    @classmethod
    def register_platform(cls, name, platform_class):
        cls.PLATFORMS[name] = platform_class

    @staticmethod
    def parse(text):
        """Extract social media objects from user text.

        Args:
            text (str):

        Returns:
            List[SocialMedia]: List of social media objects
        """
        social_media = []
        # simple text pre-processing
        # normalize unicode to ascii, e.g. mathematical 𝐈 to the actual letter I
        text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')
        # remove "is" using `re.sub`
        text = re.sub(r"\bis\b", " ", text)
        # remove repeated whitespaces
        text = re.sub(r'\s+', ' ', text)
        for platform_class in SocialMedia.PLATFORMS.values():
            # iterate over all regexes
            for regex in platform_class.USERNAME_REGEXES:
                # if USERNAME_CASE_SENSITIVE is False, add the `re.IGNORECASE` flag
                if not platform_class.USERNAME_CASE_SENSITIVE:
                    regex = re.compile(regex, re.IGNORECASE)
                else:
                    regex = re.compile(regex)
                # only 1 match per social media is allowed, because we're in a typical flow of scanning a profile page
                match = re.search(regex, text)
                if match:
                    # remove matched substring from text to prevent analyzing the same texts multiple times
                    text = text.replace(match.group(0), "")
                    username = match.group("username")
                    platform = platform_class(username)
                    social_media.append(platform)
                    break

        return social_media
