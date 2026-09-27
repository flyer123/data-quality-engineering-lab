
import pandas as pd

from validation.rules.regex import RegexRule


def test_fail_when_one_value_doesn_not_match() -> None:
    df = pd.DataFrame(
            {'zip_code' : ['99999-999', '12345-123', '34-567', '44333-555']}
        )
    
    rule = RegexRule("zip_code", r'^\d{5}-\d{3}$')

    
    result = rule.validate(df, "test_regex")
  
    assert result.failed_rows == 1
    assert result.passed is False

def test_pass_when_one_value_is_null() -> None:
    df = pd.DataFrame(
            {'zip_code' : ['99999-999', '12345-123', None, '44333-555']}
        )
    
    rule = RegexRule("zip_code", r'^\d{5}-\d{3}$')

    
    result = rule.validate(df, "test_regex")
  
    assert result.failed_rows == 0
    assert result.passed is True

def test_pass_when_all_values_match() -> None:
    df = pd.DataFrame(
            {'zip_code' : ['99999-999', '12345-123', '44333-555']}
        )
    
    rule = RegexRule("zip_code", r'^\d{5}-\d{3}$')

    
    result = rule.validate(df, "test_regex")
  
    assert result.failed_rows == 0
    assert result.passed is True

def test_fail_when_all_values_do_not_match() -> None:
    df = pd.DataFrame(
            {'zip_code' : ['99999-99', '1245-123', '4433-555']}
        )
    
    rule = RegexRule("zip_code", r'^\d{5}-\d{3}$')

    
    result = rule.validate(df, "test_regex")
  
    assert result.failed_rows == 3
    assert result.passed is False

def test_fail_when_value_is_empty() -> None:
    df = pd.DataFrame(
        {"zip_code": ["99999-999", "", "44433-555"]}
    )

    rule = RegexRule("zip_code", r'^\d{5}-\d{3}$')

    result = rule.validate(df, "test_regex")
      
    assert result.failed_rows == 1
    assert result.passed is False