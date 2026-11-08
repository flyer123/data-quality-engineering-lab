import pandas as pd

from ..base import ValidationRule
from ..result import ValidationResult


class RegexRule(ValidationRule):
    def __init__(self, column: str, pattern: str) -> None:
        super().__init__(column)
        self.pattern = pattern

    def validate(
        self,
        data: pd.DataFrame,
        dataset: str,
    ) -> ValidationResult:
        series = data[self.column]
        invalid_mask = (
            series.notna()
            & ~series.str.fullmatch(self.pattern, na=False)
        )
        failed_rows = int(invalid_mask.sum())

        passed = failed_rows == 0

        if passed:
            message = (
                f"{self.column} contains no values that don't "
                "match the required pattern"
            )
        else:
            message = (
                f"{self.column} contains {failed_rows} "
                "values that don't match the required pattern"
            )

        return ValidationResult(
            "Regex",
            dataset,
            self.column,
            passed,
            failed_rows,
            message,
        )