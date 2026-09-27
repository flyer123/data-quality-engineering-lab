import pandas as pd

from validation.rules.accepted import AcceptedValuesRule


def test_fail_when_one_value_is_not_accepted() -> None:
    df = pd.DataFrame(
            {"order_status" : ['delivered','shipped','banana','processing']}
        )
    
    rule = AcceptedValuesRule("order_status", ['delivered','shipped','processing'])

    
    result = rule.validate(df, "test_accepted")
  
    assert result.failed_rows == 1
    assert result.passed is False

def test_fail_when_all_values_are_not_accepted() -> None:
    df = pd.DataFrame(
            {"order_status" : ['apple','pinaple','banana','grape']}
        )
    
    rule = AcceptedValuesRule("order_status", ['delivered','shipped','processing'])

    
    result = rule.validate(df, "test_accepted")
  
    assert result.failed_rows == 4
    assert result.passed is False

def test_pass_when_all_values_accepted_accepted() -> None:
    df = pd.DataFrame(
            {"order_status" : ['delivered','shipped','shipped','processing']}
        )
    
    rule = AcceptedValuesRule("order_status", ['delivered','shipped','processing'])

    
    result = rule.validate(df, "test_accepted")
  
    assert result.failed_rows == 0
    assert result.passed is True

def test_ignore_null_values() -> None:
    df = pd.DataFrame(
        {"order_status": ["delivered", None, "shipped"]}
    )

    rule = AcceptedValuesRule(
        "order_status",
        ["delivered", "shipped", "processing"],
    )

    result = rule.validate(df, "test_accepted")

    assert result.failed_rows == 0
    assert result.passed is True