from dataclasses import dataclass


@dataclass
class SearchRequest:
    """Class for keeping track of an item in inventory."""

    def __init__(self):
        pass

    keyword: str