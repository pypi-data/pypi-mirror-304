import re

PACKAGE_AND_VERSION_PATTERN = re.compile(r'(?P<name>[a-zA-Z0-9]([a-zA-Z0-9_-]*[a-zA-Z0-9])?)(?P<version>.*)')
