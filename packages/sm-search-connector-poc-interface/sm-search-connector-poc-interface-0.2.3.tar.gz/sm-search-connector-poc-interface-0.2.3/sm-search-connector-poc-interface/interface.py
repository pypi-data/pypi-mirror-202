from abc import ABC, abstractmethod
from searchRequest import SearchRequest
from searchResponse import SearchResponse


class ISearchConnector(ABC):
    """
    A search interface for search connector
    """

    @abstractmethod
    def search(self, request: SearchRequest) -> SearchResponse:
        pass
