import random

from deap import creator

from slice_finder.slice_finders.slice_finder import SliceFinder
from slice_finder.types import Filter


class GASliceFinder(SliceFinder):
    """Slice discovery using Genetic algorithm."""

    def create_individual(self, n_filters: int | tuple[int, int]):
        return creator.Individual(self.data_structure.get_n_filters(n_filters))

    def mutate_individual(self, individual: list[Filter], indpb: float):
        for i in range(len(individual)):
            if random.random() < indpb:
                individual[i] = self.data_structure.get_filter()
        return (individual,)

    def eval_individual(
        self,
        individual: list[Filter],
        **kwargs,
    ):
        df = self.data_connector.filter(self.data_connector.data, individual)
        if len(df) < len(self.data_connector.data) * kwargs["min_size"]:
            return None
        return (kwargs["metric"](df),)
