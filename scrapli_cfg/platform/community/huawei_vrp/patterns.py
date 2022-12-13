import re

VERSION_PATTERN = re.compile(
    # should match at least version like:
    #
    r"Version (?P<version>.*?(?=\s\(+))"
)