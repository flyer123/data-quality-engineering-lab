import pandas as pd

from validation.base import ValidationRule
from validation.result import ValidationResult


class ValidationRunner:
    def __init__(self, configured_rules: list[ValidationRule])-> None:
        self.configured_rules = configured_rules
        if len(configured_rules) == 0:
            raise ValueError("Add at least one data validation rule")
        

    def run_validation(self, data: pd.DataFrame, dataset: str) -> list[ValidationResult] :
        
        results: list[ValidationResult] = []
        for rule in self.configured_rules:
            results.append(rule.validate(data, dataset))
        return results
            
