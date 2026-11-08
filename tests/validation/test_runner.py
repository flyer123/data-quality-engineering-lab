import pandas as pd
import pytest

from validation.base import ValidationRule
from validation.rules.not_null import NotNullRule
from validation.rules.range import RangeRule

#from validation.result import ValidationResult
from validation.validation_runner import ValidationRunner


def test_one_rule_failed() -> None:
    df = pd.DataFrame(
            {'customer_id' : ['C001', 'C002', None, 'C004']}
        )
    
    not_null_rule = NotNullRule("customer_id")
    rules_set: list[ValidationRule] = []
    rules_set.append(not_null_rule)

    runner = ValidationRunner(rules_set)
    test_results = runner.run_validation(df, "orders")
    assert test_results[0].passed is False

def test_runner_executes_multiple_rules() -> None:
    df = pd.DataFrame(
                {
                    'customer_id' : ['C001', 'C002', None, 'C004'],
                    'payment_value' : [25.50, 70.00, 0.00, 30.00]
                    }
            )
    not_null_rule = NotNullRule("customer_id")
    range_rule = RangeRule("payment_value", 0.00, 80.00)
    rules_set: list[ValidationRule] = []
    rules_set.append(not_null_rule)
    rules_set.append(range_rule)

    runner = ValidationRunner(rules_set)
    test_results = runner.run_validation(df, "orders")
    assert test_results[0].passed is False
    assert test_results[1].passed is True
    assert len(test_results) == 2
    assert test_results[0].rule_name == 'NotNull'
    assert test_results[1].rule_name == 'Range'
    assert test_results[0].failed_rows == 1

def test_empty_rule_collection_failed() -> None:
        
    rules_set: list[ValidationRule] = []
    
    with pytest.raises(ValueError, match='Add at least one data validation rule'):
        ValidationRunner(rules_set)

def test_runner_reuse_success() -> None:
    df_fail = pd.DataFrame(
                {'customer_id' : ['C001', 'C002', None, 'C004']}
            )
    df_pass = pd.DataFrame(
                {'customer_id' : ['C001', 'C002', 'C003', 'C004']}
            )
    not_null_rule = NotNullRule("customer_id")
    rules_set: list[ValidationRule] = []
    rules_set.append(not_null_rule)
    
    runner = ValidationRunner(rules_set)
    test_results_fail = runner.run_validation(df_fail, "orders")
    assert test_results_fail[0].passed is False
    assert test_results_fail[0].failed_rows == 1

    test_results_pass = runner.run_validation(df_pass, "orders")
    assert test_results_pass[0].passed is True
    assert test_results_pass[0].failed_rows == 0
    assert len(test_results_pass) == 1
    assert len(test_results_fail) == 1
    assert test_results_fail is not test_results_pass
    assert test_results_fail[0].passed is False
    assert test_results_fail[0].failed_rows == 1

def test_dataframe_integrity() -> None:
    df = pd.DataFrame(
                    {'customer_id' : ['C001', 'C002', None, 'C004']}
                )
    df_copy = df.copy()
    not_null_rule = NotNullRule("customer_id")
    rules_set: list[ValidationRule] = []
    rules_set.append(not_null_rule)
    
    runner = ValidationRunner(rules_set)
    runner.run_validation(df_copy, "orders")
    pd.testing.assert_frame_equal(df, df_copy)
