from dataclasses import dataclass


@dataclass
class SearchResponse:
    """Class for keeping track of an item in inventory."""

    def __init__(self):
        pass

    datasetId: list[str]