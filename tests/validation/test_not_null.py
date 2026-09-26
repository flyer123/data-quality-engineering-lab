import pandas as pd

from validation.rules.not_null import NotNullRule


def test_fail_when_value_is_null() -> None:
    df = pd.DataFrame(
        {'customer_id' : ['C001', 'C002', None, 'C004']}
    )

    rule = NotNullRule("customer_id")

    result = rule.validate(df, "test_null_customer")

    assert result.failed_rows == 1
    assert result.passed is False

def test_not_null_passes_when_no_values_are_null() -> None:
    df = pd.DataFrame(
            {'customer_id' : ['C001', 'C002', 'C003', 'C004']}
        )
    rule = NotNullRule("customer_id")

    result = rule.validate(df, "test_not_null_customer")

    assert result.failed_rows == 0
    assert result.passed is True

def test_not_null_fails_when_all_values_are_null() -> None:
    df = pd.DataFrame(
            {'customer_id' : [None, None, None]}
        )

    rule = NotNullRule("customer_id")

    result = rule.validate(df, "test_all_null_customer")

    assert result.failed_rows == 3
    assert result.passed is False
    
