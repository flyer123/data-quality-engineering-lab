from ..base import ValidationRule
from ..result import ValidationResult


class RangeRule(ValidationRule):
    def __init__(self, column, min_value: float, max_value: float | None = None) -> None:
        super().__init__(column)
        if max_value is not None and min_value > max_value:
            raise ValueError(
                "min_value cannot be greater than max_value"
            )


        self.min_value = min_value
        self.max_value = max_value

    def validate(self, data, dataset) -> ValidationResult:
        if self.max_value is None:
            failed_rows = len(data[
                data[self.column] < self.min_value
                ])
        else:
            failed_rows = len(data[(
                data[self.column] < self.min_value
                ) | (
                    data[self.column] > self.max_value
                )
                ])

        passed = failed_rows == 0

        if passed:
            message = (f"{self.column} contains no values outside"
                       f"the configured range"
            )
        else:
            message = f"{self.column} contains {failed_rows} "
            "values outside the configured range"

            
        return ValidationResult(
                                'Range', 
                                dataset, 
                                self.column, 
                                passed, 
                                failed_rows, 
                                message,
                                )   
                                