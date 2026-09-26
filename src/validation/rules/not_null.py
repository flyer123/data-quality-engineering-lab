from ..base import ValidationRule
from ..result import ValidationResult


class NotNullRule(ValidationRule):


    def validate(self, data, dataset) -> ValidationResult:
        failed_rows = int(data[self.column].isna().sum())
        passed = failed_rows == 0

        if passed:
            message = f"{self.column} contains no NULL values"
        else:
            message = f"{self.column} contains {failed_rows} NULL values"

  
        return ValidationResult(
            'NotNull', 
            dataset, 
            self.column, 
            passed, 
            failed_rows, 
            message,
        )