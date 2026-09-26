from ..base import ValidationRule


class AcceptedValuesRule(ValidationRule):
    def __init__(self, column, accepted_values: list[str]) -> None:
        super().__init__(column)