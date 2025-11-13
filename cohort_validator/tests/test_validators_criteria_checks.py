"""
Unit tests for validators/criteria_checks.py - Focused on key checkers
"""

import pytest
from cohort_validator.models.cohort import CohortExpression
from cohort_validator.models.criteria import (
    Criteria,
    CriteriaGroup,
    ConditionOccurrence,
)
from cohort_validator.validators.criteria_checks import (
    EmptyPrimaryCriteriaValueCheck,
    RangeCheck,
    TextCheck,
)


class TestRangeCheck:
    """Tests for RangeCheck."""

    def test_range_check_with_valid_cohort(self):
        """Test RangeCheck with valid cohort."""
        check = RangeCheck()
        expression = CohortExpression()
        warnings = check.check(expression)
        assert isinstance(warnings, list)


class TestTextCheck:
    """Tests for TextCheck manager."""

    def test_text_check_with_valid_cohort(self):
        """Test TextCheck with valid cohort."""
        check = TextCheck()
        expression = CohortExpression()
        warnings = check.check(expression)
        assert isinstance(warnings, list)


class TestEmptyPrimaryCriteriaValueCheck:
    """Tests for EmptyPrimaryCriteriaValueCheck."""

    def test_empty_primary_criteria_value_check(self):
        """Test EmptyPrimaryCriteriaValueCheck."""
        check = EmptyPrimaryCriteriaValueCheck()
        expression = CohortExpression()
        warnings = check.check(expression)
        assert isinstance(warnings, list)

    def test_empty_primary_criteria_with_criteria(self):
        """Test with primary criteria that has values."""
        from cohort_validator.models.cohort import PrimaryCriteria

        check = EmptyPrimaryCriteriaValueCheck()
        expression = CohortExpression(
            primary_criteria=PrimaryCriteria(
                criteria_list=[
                    Criteria(condition_occurrence=ConditionOccurrence(codeset_id=0))
                ]
            )
        )
        warnings = check.check(expression)
        assert isinstance(warnings, list)

