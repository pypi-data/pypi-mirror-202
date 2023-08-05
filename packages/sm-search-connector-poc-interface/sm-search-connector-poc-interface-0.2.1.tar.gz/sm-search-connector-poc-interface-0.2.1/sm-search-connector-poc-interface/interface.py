from abc import ABC, abstractmethod


class ISearchConnector(ABC):
    """
    A search interface for search connector
    """

    @abstractmethod
    def search(self, request) -> str:
        pass
