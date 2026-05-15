import fnmatch
from typing import Protocol


class Matcher(Protocol):

    def matches(self, value) -> bool:
        ...


class Wildcard(Matcher):

    def __init__(self, value: str):
        self.value = value

    def matches(self, other: str):
        return fnmatch.fnmatch(other, self.value)
