import os
import importlib
from .base import SocialMedia

# Dynamically import all social media plugins in this directory
files = os.listdir(os.path.dirname(__file__))
# some regexes are conflicting, at least ensure predictable order
files_sorted = sorted(files)
for file in files_sorted:
    if file.endswith('.py') and file != '__init__.py':
        module_name = file[:-3]
        module = importlib.import_module('.' + module_name, package=__name__)
        for name in dir(module):
            obj = getattr(module, name)
            if isinstance(obj, type) and issubclass(obj, SocialMedia) and obj != SocialMedia:
                SocialMedia.register_platform(obj.PLATFORM_NAME, obj)
