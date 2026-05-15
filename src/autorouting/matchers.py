"""Collection of ready-to-use URL requirement matchers.
"""

import fnmatch
from typing import Protocol


class Matcher(Protocol):
    """URL requirement matcher protocol.
    """

    def matches(self, value) -> bool:
        """Test the value against the matching needs and returns a boolean.
        """


class Wildcard(str):
    """Wildcard requirement matcher based on `fnmatch`.
    """
    def matches(self, value: str):
        """Matches the value against a `fnmatch` pattern.
        """
        return fnmatch.fnmatch(value, self)
