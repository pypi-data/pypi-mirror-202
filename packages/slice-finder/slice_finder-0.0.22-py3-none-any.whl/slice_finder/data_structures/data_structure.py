from abc import abstractmethod
import random

from slice_finder.data_connectors.data_connector import DataConnector


class DataStructure:
    @abstractmethod
    def init(
        self,
        data_connector: DataConnector,
        verbose: bool,
        random_state: int | None,
    ):
        """This function will run in the __init__ of the the SliceFinder."""

        raise NotImplementedError()

    @abstractmethod
    def get_filter(self):
        """Get Filter object."""

        raise NotImplementedError()

    def get_n_filters(self, n_filters: int | tuple[int, int]):
        """Get n filter objects."""

        if isinstance(n_filters, tuple):
            n_filters = random.randint(n_filters[0], n_filters[1])
        return [self.get_filter() for _ in range(n_filters)]
