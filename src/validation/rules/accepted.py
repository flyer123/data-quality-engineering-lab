import pandas as pd

from ..base import ValidationRule
from ..result import ValidationResult


class AcceptedValuesRule(ValidationRule):
    def __init__(self, column: str, accepted_values: list[str]) -> None:
        super().__init__(column)
        self.accepted_values = accepted_values

    def validate(self, data: pd.DataFrame, dataset: str) -> ValidationResult:
        failed_rows = len(data[
                        data[self.column].notna()
                        & ~data[self.column].isin(self.accepted_values)
                        ])
        passed = failed_rows == 0

        if passed:
            message = (f"{self.column} contains no values outside "
                      "the list of allowed values"
                    )
        else:
            message = (f"{self.column} contains {failed_rows} "
                      "values outside the list of allowed values"
            )
                           
        return ValidationResult(
                                'AcceptedValues', 
                                dataset, 
                                self.column, 
                                passed, 
                                failed_rows, 
                                message,
                                )   