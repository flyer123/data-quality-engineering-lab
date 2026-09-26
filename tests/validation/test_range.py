import pandas as pd

from validation.rules.range import RangeRule


def test_fail_when_outside_range_min_max() -> None:
    df = pd.DataFrame(
            {'payment_value' : [25.50, 100.00, -5.00, 30.00]}
        )
    
    rule = RangeRule("payment_value", 0.00, 80.00)

    
    result = rule.validate(df, "test_range")
  
    assert result.failed_rows == 2
    assert result.passed is False

def test_fail_when_outside_range_min() -> None:
    df = pd.DataFrame(
            {'payment_value' : [25.50, 100.00, -5.00, 30.00]}
        )
    
    rule = RangeRule("payment_value", 0.00)

    
    result = rule.validate(df, "test_range")
  
    assert result.failed_rows == 1
    assert result.passed is False

def test_fail_when_all_outside_range_min_max() -> None:
    df = pd.DataFrame(
            {'payment_value' : [25.50, 100.00, 15.00, 30.00]}
        )
    
    rule = RangeRule("payment_value", 0.00, 10.00)

    
    result = rule.validate(df, "test_range")
  
    assert result.failed_rows == 4
    assert result.passed is False


def test_pass_when_in_range_min_max() -> None:
    df = pd.DataFrame(
            {'payment_value' : [25.50, 100.00, 5.00, 30.00]}
        )
    
    rule = RangeRule("payment_value", 0.00, 200.00)

    
    result = rule.validate(df, "test_range")
  
    assert result.failed_rows == 0
    assert result.passed is True

def test_pass_when_bigger_than_min() -> None:
    df = pd.DataFrame(
            {'payment_value' : [25.50, 100.00, 5.00, 30.00]}
        )
    
    rule = RangeRule("payment_value", 0.00)

    
    result = rule.validate(df, "test_range")
  
    assert result.failed_rows == 0
    assert result.passed is True

def test_pass_when_values_equal_boundaries() -> None:
    df = pd.DataFrame(
            {'payment_value' : [0.00, 50.00, 100.00]}
        )
    
    rule = RangeRule("payment_value", 0.00, 100.00)

    
    result = rule.validate(df, "test_range")
  
    assert result.failed_rows == 0
    assert result.passed is True

def test_fail_when_value_above_max() -> None:
    df = pd.DataFrame(
            {'payment_value' : [20.00,50.00, 101.00]}
        )
    
    rule = RangeRule("payment_value", 0.00, 100.00)

    
    result = rule.validate(df, "test_range")
  
    assert result.failed_rows == 1
    assert result.passed is False

def test_range_rejects_invalid_configuration() -> None:
    try:
        RangeRule("payment_value", 100.00, 0.00)
        assert False
    except ValueError:
        pass