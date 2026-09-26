from abc import ABC, abstractmethod

import pandas as pd

from .result import ValidationResult


class ValidationRule(ABC):
    def __init__(self, column: str) -> None:
        self.column = column


    @abstractmethod
    def validate(self, data: pd.DataFrame, dataset: str) -> ValidationResult:
        """Validate data and return a ValidationResult."""
        ...