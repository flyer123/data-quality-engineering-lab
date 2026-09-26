from dataclasses import dataclass


@dataclass
class ValidationResult:
    rule_name: str
    dataset: str
    column: str
    passed: bool
    failed_rows: int
    message: str