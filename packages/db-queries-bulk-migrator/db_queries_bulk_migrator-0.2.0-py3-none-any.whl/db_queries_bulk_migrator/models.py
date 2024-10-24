from typing import List, Dict, Optional
import sqlparse

class CustomDBQuery:
    def __init__(
        self,
        name: str,
        schedule: str,
        value: str,
        value_columns: Optional[List[str]] = [],
        dimension_columns: Optional[List[str]] = [],
        extra_dimensions: Optional[List] = [],
    ) -> None:
        self.name = f"{name}"
        self.schedule = schedule
        self.value = value.replace("\n", " ")
        self.value_columns = value_columns
        self.dimension_columns = dimension_columns
        self.extra_dimensions = extra_dimensions
