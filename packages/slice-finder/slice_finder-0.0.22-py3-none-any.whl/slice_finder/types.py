from dataclasses import dataclass
from typing import Any


@dataclass
class Filter:
    """Filter object."""

    feature: str
    operator: str
    value: str | float | bool


@dataclass
class Extreme:
    """Extreme object."""

    data_metric_value: float
    filtered_data: Any
    filtered_data_metric_value: float
    filters: list[Filter]

    def get_human_readable(self) -> str:
        """Returns a human readable format of the object.

        Returns:
            Human readable object.
        """

        textual_filters = [
            f"{filter.feature} {filter.operator} {filter.value}" for filter in self.filters
        ]
        textual_composite_filter = "\nAND ".join(textual_filters)
        return f"""When {textual_composite_filter},
the value of the metric on the filtered data is {self.filtered_data_metric_value}
compared to {self.data_metric_value} on the whole data.
"""

    def __str__(self) -> str:
        return self.get_human_readable()

    def __repr__(self) -> str:
        return self.get_human_readable()
